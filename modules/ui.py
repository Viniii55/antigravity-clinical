import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;600;800&display=swap');
        
        /* --- AURORA BACKGROUND ANIMATION --- */
        @keyframes aurora {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #0f172a);
            background-size: 400% 400%;
            animation: aurora 15s ease infinite;
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3, h4, .stMarkdown {
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: -0.5px;
        }
        
        p, div, label, input, textarea, button {
            font-family: 'Inter', sans-serif !important;
        }

        /* --- DEEP GLASS CARDS --- */
        .premium-card {
            background: rgba(17, 24, 39, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 1px solid rgba(255, 255, 255, 0.15); /* Light reflection on top */
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
            margin-bottom: 24px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .premium-card:hover {
            transform: translateY(-4px) scale(1.005);
            background: rgba(23, 31, 50, 0.8);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 30px 60px rgba(99, 102, 241, 0.15);
        }

        /* --- NEON BUTTONS --- */
        div.stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 16px 32px;
            border-radius: 16px;
            font-weight: 600;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
        }
        
        div.stButton > button:hover {
            opacity: 1;
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(124, 58, 237, 0.6);
            border-color: rgba(255,255,255,0.3);
        }
        
        div.stButton > button:active {
            transform: scale(0.98);
        }

        /* --- HUD INPUTS --- */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #e2e8f0 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"]:hover {
            border-color: #818cf8 !important;
            background: rgba(15, 23, 42, 0.9) !important;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
        }

        /* --- METRICS --- */
        [data-testid="stMetricValue"] {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            background: -webkit-linear-gradient(#c084fc, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* --- SIDEBAR POLISH --- */
        [data-testid="stSidebar"] {
            background-color: #0b0f19;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        /* Hiding Streamlit Boilerplate */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def render_hero():
    # Tenta carregar a imagem de perfil
    import os
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Profile Picture Container
        img_path = "assets/profile.png"
        if not os.path.exists(img_path):
            img_path = "assets/profile.jpg" # tenta jpg
            
        if os.path.exists(img_path):
            st.image(img_path, width=130)
        else:
            # Placeholder se não tiver foto ainda
            st.markdown("""
                <div style='
                    width: 120px; height: 120px; 
                    background: linear-gradient(135deg, #312e81, #4c1d95); 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                    border: 3px solid rgba(99, 102, 241, 0.5);
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
                    font-size: 3rem;'>
                    🧠
                </div>
            """, unsafe_allow_html=True)

    with col2:
        # Typography Hero
        st.markdown("""
            <div style='display: flex; flex-direction: column; justify-content: center; height: 100%; padding-left: 10px;'>
                <h1 style='
                    font-family: "Outfit", sans-serif;
                    font-size: 4.2rem; 
                    font-weight: 800;
                    margin: 0;
                    background: -webkit-linear-gradient(0deg, #ffffff 10%, #a5b4fc 90%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    text-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
                '>Dr. Rodrigo Gomes</h1>
                <p style='
                    color: #cbd5e1; 
                    font-size: 1.3rem; 
                    font-weight: 600; 
                    letter-spacing: 2px; 
                    text-transform: uppercase;
                    margin-top: -5px;
                    display: flex; align-items: center; gap: 12px;
                '>
                    <span style='color: #818cf8; font-size: 1.5rem;'>•</span> Neuropsicologia Clínica <span style='color: #818cf8; font-size: 1.5rem;'>•</span> CRM: 05/59056
                </p>
                <div style='margin-top: 15px; display: inline-block;'>
                    <span style='
                        background: rgba(99, 102, 241, 0.15); 
                        color: #a5b4fc; 
                        padding: 6px 14px; 
                        border-radius: 20px; 
                        font-size: 0.85rem; 
                        border: 1px solid rgba(99, 102, 241, 0.3);'>
                        ✨ Antigravity v2.1 Online
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

def render_metrics(num_images, has_audio):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Imagens", f"{num_images}", delta="Lote Atual" if num_images > 0 else None)
    with col2:
        status = "Pronto" if has_audio else "Aguardando"
        st.metric("Áudio", status, delta_color="normal" if has_audio else "off")
    with col3:
        st.metric("Modelo", "OMNI-4o", "Ativo")
