import streamlit as st
import io
import time
from modules.backend import AntigravityEngine
from modules.ui import load_custom_css, render_hero, render_metrics
from modules.document_gen import DocumentGenerator

# --- App Configuration ---
st.set_page_config(
    page_title="Tradutor Clínico | Dr. Rodrigo Gomes",
    page_icon="🧠",
    layout="wide", # Switching to wide for better workspace
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
    st.image("https://img.icons8.com/3d-fluency/94/brain.png", width=60)
    st.markdown("### **Tradutor Clínico**")
    st.caption("v2.1 Hybrid Engine")
    
    st.markdown("---")
    
    # --- CONFIGURAÇÃO SILENCIOSA (Hardcoded) ---
    # O usuário pediu para esconder a seleção.
    # Padrão: Google Gemini 1.5 Flash (Grátis)
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

# Input Section (Glass Card)
with st.container():
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Central de Upload")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        uploaded_images = st.file_uploader(
            "Anexar Anotações (Manuscritos)", 
            type=['png', 'jpg', 'jpeg'], 
            accept_multiple_files=True
        )
        
    with col2:
        uploaded_audio = st.file_uploader(
            "Anexar Áudio (Resumo)", 
            type=['mp3', 'ogg', 'wav', 'm4a']
        )
        
    render_metrics(len(uploaded_images) if uploaded_images else 0, uploaded_audio is not None)
    st.markdown('</div>', unsafe_allow_html=True)

# Action Section
generate_btn = st.button("✨ INICIAR TRADUÇÃO CLÍNICA", type="primary")

if generate_btn:
    if not uploaded_images and not uploaded_audio:
        st.error("⚠️ O sistema precisa de pelo menos uma fonte de dados (Imagem ou Áudio).")
        st.stop()
        
    with st.status("🧠 O Neural Engine está trabalhando...", expanded=True) as status:
        try:
            # 1. Audio Phase
            transcript = ""
            if uploaded_audio:
                st.write("🎙️ Ouvindo e transcrevendo áudio...")
                transcript = engine.transcribe_audio(uploaded_audio)
                st.write("✅ Áudio decodificado.")
            
            # 2. Vision & Reasoning Phase
            st.write("👁️ Analisando manuscritos e correlacionando fatos...")
            final_report = engine.generate_clinical_report(transcript, uploaded_images if uploaded_images else [])
            
            if final_report:
                st.session_state['generated_doc'] = final_report
                # Add to history
                from datetime import datetime
                st.session_state['history'].append({
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "content": final_report
                })
                status.update(label="✅ Processamento Finalizado!", state="complete", expanded=False)
            
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
