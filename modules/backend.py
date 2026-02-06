import openai
import google.generativeai as genai
from PIL import Image
import io
import base64
import streamlit as st
import time

class AntigravityEngine:
    def __init__(self, api_key, provider="openai"):
        self.provider = provider
        self.api_key = api_key
        
        if provider == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        elif provider == "google":
            genai.configure(api_key=api_key)
            # Usando "gemini-1.5-flash" pois é o modelo Tier Free mais estável e rápido atualmente
            self.client = genai.GenerativeModel('gemini-1.5-flash')

    @staticmethod
    def encode_image_base64(image_bytes):
        return base64.b64encode(image_bytes).decode('utf-8')

    @staticmethod
    def resize_image(image_file, max_size=1536):
        """
        Resizes image intelligently. 
        Increased max_size for better OCR readability on medical notes.
        """
        img = Image.open(image_file)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        width, height = img.size
        # Resize only if drastically larger, to preserve handwriting details
        if max(width, height) > max_size:
            ratio = max_size / max(width, height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=95) 
        return buffered.getvalue()

    def transcribe_audio(self, audio_file):
        """Transcribes audio using Whisper (OpenAI) or returns file for Gemini."""
        if self.provider == "openai":
            try:
                audio_file.seek(0)
                transcript_response = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    prompt="Termos médicos, neuropsicologia, anamnese, paciente, avaliação."
                )
                return transcript_response.text
            except Exception as e:
                st.error(f"Erro na transcrição de áudio (OpenAI): {e}")
                return ""
        elif self.provider == "google":
            # For Gemini, we don't necessarily need to pre-transcribe if we use multimodal input,
            # but to keep the flow consistent, we can return the file object to be used in generation.
            # However, Streamlit file objects need to be handled carefully.
            # For this version, let's treat Gemini audio as "Multimodal Context" in the generation phase.
            return "[Áudio anexado para processamento multimodal nativo]"

    def generate_clinical_report(self, transcript, images, audio_file=None):
        """
        Core logic for generating the report using either GPT-4o or Gemini 1.5 Pro.
        """
        system_prompt = """
# ROLE
You are the elite Assistant for Neuropsychologist Dr. Rodrigo Abel Gomes.
Your Goal: Convert handwritten notes images + audio into a specific document format called "História Clínica".

# CRITICAL RULES (DO NOT IGNORE)
1. **NO HALLUCINATIONS (OCR SAFETY):** 
   - Handwritten text context is PSYCHOLOGY/BEHAVIOR. 
   - If a word looks like "fresquinha" but context is "falar", it is likely "vergonha" or "frustração". 
   - If you are not 100% sure, write "[ilegível]" instead of guessing/inventing a word.
   - WATCH OUT for: "competitivo" (do NOT say encorajar se o texto diz competitivo), dates (Data de registro vs Nascimento).

2. **STRICT STRUCTURE (THE "THOMAS" TEMPLATE):**
   - Block 1: **IDENTIFICAÇÃO** (List format: Paciente, Idade, Nascimento, Pais, Escola).
   - Block 2: **HISTÓRIA CLÍNICA** (Narrative prose ONLY).
   - **FORBIDDEN:** Do NOT use subheaders like "Queixa Principal", "Histórico Social", "Conclusão" inside the History section. Write cohesive paragraphs like a book chapter.

3. **LOGICAL FLOW (Rodrigo's Standard):**
   - Paragraph 1: Referral reason (Encaminhamento) & Main Complaint.
   - Paragraph 2: Pregnancy, Birth, Early Development (walking, talking, eating).
   - Paragraph 3: Medical/Sensory history (surgeries, hearing, tics).
   - Paragraph 4: Current Behavior (Socialization, Agitation, Stereotypies - include specific durations like '4h spinning', 'gira sem parar').
   - Paragraph 5: Academic/School context.
   - Paragraph 6: Family dynamics & Routine (Sleep, Hygiene).

4. **DATA CORRECTION:**
   - If the note says "12/12/2019" and age is "5 years", that is the **Data de nascimento**, not registration.
   - Arrow "->" means "leads to", "results in", or "consequently".
   - "Ñ" means "Não". "c/" means "com".

# TONE CHECK
- Use formal, third-person clinical Portuguese.
- Bad: "Ele tem vergonha." -> Good: "Relata-se inibição social e timidez."
- Bad: "Gira 4h." -> Good: "Apresenta estereotipias motoras de longa duração (ex: girar o corpo por até 4 horas)."
- Do not summarize too much. Keep specific details like "cirurgia de adenoide" ou "quer ser melhor que os outros" (competitividade).

# FINAL OUTPUT FORMAT
(Produce exactly this structure. No extra formatted titles.)

**IDENTIFICAÇÃO**
**Paciente:** [Name]
**Idade:** [Age] (durante a avaliação).      **Data de nascimento:** [Date]
**Escolaridade:** [School info]
**Nome dos responsáveis:** [Parents]

**História Clínica:**
[Insert the cohesive narrative text here, comprising about 6-8 paragraphs following the logical flow defined above. No bullet points, no bold subtitles within the text.]
"""
        
        # --- OPENAI LOGIC ---
        if self.provider == "openai":
            user_content = []
            if transcript:
                user_content.append({"type": "text", "text": f"### AUDIO TRANSCRIPT (CONTEXT):\n{transcript}"})
            
            for img_file in images:
                img_bytes = self.resize_image(img_file)
                b64_img = self.encode_image_base64(img_bytes)
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64_img}", "detail": "high"}
                })
                
            if not user_content: return None

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    max_tokens=2500,
                    temperature=0.4
                )
                return response.choices[0].message.content
            except Exception as e:
                st.error(f"Erro na geração (OpenAI): {e}")
                return None

        # --- GOOGLE GEMINI LOGIC (DYNAMIC DISCOVERY) ---
        elif self.provider == "google":
            chosen_model_name = None
            
            try:
                # 1. Perguntar ao Google quais modelos temos acesso
                available_models = list(genai.list_models())
                
                # 2. Filtrar apenas os que geram conteúdo (chat/vision)
                valid_models = [m for m in available_models if 'generateContent' in m.supported_generation_methods]
                
                # 3. Escolher o melhor (Prioridade: Flash > Pro > Qualquer outro 1.5 > Qualquer outro)
                model_priority = ['flash', 'pro', '1.5']
                
                for priority in model_priority:
                     for m in valid_models:
                         if priority in m.name.lower():
                             chosen_model_name = m.name
                             break
                     if chosen_model_name: break
                
                # Fallback: Se não achou nenhum com os nomes acima, pega o primeiro válido
                if not chosen_model_name and valid_models:
                    chosen_model_name = valid_models[0].name
                
                if not chosen_model_name:
                    st.error("Sua chave API não tem acesso a nenhum modelo de geração de texto/imagem.")
                    return None

                # 4. Executar com o modelo escolhido
                # st.info(f"Usando modelo detectado: {chosen_model_name}") # Uncomment for debug
                model = genai.GenerativeModel(chosen_model_name)
                
                inputs = [system_prompt]
                for img_file in images:
                    img_bytes = self.resize_image(img_file)
                    img = Image.open(io.BytesIO(img_bytes))
                    inputs.append(img)
                
                if audio_file:
                     inputs.append(f"Contexto de áudio adicional: {audio_file.name if hasattr(audio_file, 'name') else 'Audio'}")

                response = model.generate_content(inputs)
                return response.text
                
            except Exception as e:
                st.error(f"Erro Crítico (Google): {e}")
                try:
                    # Debug final para o usuário ver o que está acontecendo
                    st.code(f"Modelos Disponíveis na conta: {[m.name for m in genai.list_models()]}")
                except:
                    pass
                return None
