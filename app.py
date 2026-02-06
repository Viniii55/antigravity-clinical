import streamlit as st
import io
import time
from modules.backend import AntigravityEngine
from modules.ui import load_custom_css, render_hero, render_metrics
from modules.document_gen import DocumentGenerator

# --- App Configuration ---
st.set_page_config(
    page_title="Antigravity Clinical",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State ---
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'generated_doc' not in st.session_state:
    st.session_state['generated_doc'] = None

# --- UI Load ---
load_custom_css()

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    st.caption("v3.0 Clinical Edition")
    st.markdown("---")
    
    # --- CONFIGURAÇÃO SILENCIOSA (Hardcoded) ---
    selected_provider = "google"
    api_key = "AIzaSyCjivPedhBKpz2Jjs6Vv3t0WmySnjOQGBc"
    
    st.success(f"Sistema Online")
    st.markdown("---")
    st.markdown("#### 📜 Histórico Recente")
    for i, item in enumerate(reversed(st.session_state['history'])):
        st.text(f"• {item['timestamp']} - Laudo #{len(st.session_state['history'])-i}")

# --- Main Logic ---
render_hero()

if not api_key:
    st.error("Erro de configuração interna: Chave de API não encontrada.")
    st.stop()

engine = AntigravityEngine(api_key, provider=selected_provider)

# --- ONBOARDING HELPER ---
with st.expander("ℹ️ Guia Rápido: Como obter o melhor resultado", expanded=False):
    st.markdown("""
    - **Fotos:** Garanta que estejam legíveis, focadas e bem iluminadas.
    - **Áudio:** Resuma os pontos principais que não estão claros ou ilegíveis nas notas.
    - **Processamento:** A análise profunda pode levar até 1 minuto. Por favor, não feche a aba.
    """)

# --- MAIN INPUT SECTION (2 COLUMNS) ---
st.markdown('<div class="clinical-card">', unsafe_allow_html=True)

col_upload_1, col_upload_2 = st.columns(2, gap="large")

with col_upload_1:
    st.markdown("#### 📂 1. Imagens das Anotações")
    st.caption("Fotos do caderno, prontuário ou rascunhos.")
    uploaded_images = st.file_uploader(
        "image_uploader_hidden_label", 
        label_visibility="collapsed",
        type=['png', 'jpg', 'jpeg'], 
        accept_multiple_files=True,
        key="img_uploader"
    )
    
with col_upload_2:
    st.markdown("#### 🎙️ 2. Áudio do Caso")
    st.caption("Resumo verbal ou gravação da sessão.")
    uploaded_audio = st.file_uploader(
        "audio_uploader_hidden_label",
        label_visibility="collapsed", 
        type=['mp3', 'ogg', 'wav', 'm4a'],
        key="audio_uploader"
    )
    
st.markdown('</div>', unsafe_allow_html=True)

# --- ACTION SECTION ---
generate_btn = st.button("GERAR LAUDO CLÍNICO", type="primary", use_container_width=True)

if generate_btn:
    if not uploaded_images and not uploaded_audio:
        st.error("⚠️ O sistema precisa de pelo menos uma fonte de dados (Imagem ou Áudio).")
        st.stop()
        
    with st.spinner("Antigravity ativado: Processando e estruturando o caso clínico..."):
        try:
            # 1. Audio Phase
            transcript = ""
            if uploaded_audio:
                transcript = engine.transcribe_audio(uploaded_audio)
            
            # 2. Vision & Reasoning Phase
            final_report = engine.generate_clinical_report(transcript, uploaded_images if uploaded_images else [])
            
            if final_report:
                st.session_state['generated_doc'] = final_report
                # Add to history
                from datetime import datetime
                st.session_state['history'].append({
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "content": final_report
                })
            
        except Exception as e:
            st.error(f"Erro Crítico: {e}")
            status.update(label="❌ Falha no Processamento", state="error")

# Output Section
if st.session_state['generated_doc']:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Laudo Consolidado")
    
    col_edit, col_view = st.columns([1, 1])
    
    edited_text = st.text_area(
        "Editor em Tempo Real", 
        value=st.session_state['generated_doc'],
        height=600
    )
    
    st.markdown("---")
    
    # Generate DOCX on the fly
    docx_file = DocumentGenerator.create_word_doc(edited_text)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="💾 Baixar Documento Oficial (.docx)",
            data=docx_file,
            file_name="Laudo_Antigravity.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    with col_d2:
        if st.button("🔄 Limpar Sessão"):
            st.session_state['generated_doc'] = None
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
