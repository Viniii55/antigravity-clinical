import streamlit as st
import base64
import os

def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def load_custom_css():
    # Carregar imagem de fundo para o Banner
    header_bg = ""
    bg_path = "assets/hero.png"
    if not os.path.exists(bg_path):
        bg_path = "assets/hero.jpg"
    
    if os.path.exists(bg_path):
        img_b64 = get_img_as_base64(bg_path)
        header_bg = f"""
            background-image: linear-gradient(180deg, rgba(14, 78, 117, 0.9) 0%, rgba(14, 78, 117, 0.8) 100%), url("data:image/png;base64,{img_b64}");
            background-size: cover;
            background-position: center;
        """
    else:
        header_bg = "background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&family=Inter:wght@400;600&display=swap');
        
        /* --- GLOBAL RESET --- */
        .block-container {{
            padding-top: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }}
        
        /* --- HERO BANNER --- */
        .hero-cont {{
            {header_bg}
            padding: 4rem 1rem 6rem 1rem;
            text-align: center;
            color: white;
            margin-bottom: -4rem; /* Negative margin for overlap */
        }}
        
        /* --- FLOATING CARD --- */
        .main-content-card {{
            background: white;
            border-radius: 24px;
            padding: 2.5rem;
            max-width: 1000px;
            margin: 0 auto 2rem auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            position: relative;
            z-index: 10;
        }}
        
        /* --- TYPOGRAPHY --- */
        h1 {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800 !important;
            font-size: 3.5rem !important;
            margin-bottom: 0.5rem !important;
            color: white !important;
            text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 1.25rem;
            color: rgba(255,255,255,0.8);
            font-weight: 300;
            letter-spacing: 1px;
        }}
        
        /* --- COMPONENT OVERRIDES --- */
        .stButton button {{
            width: 100%;
            background: #0E4E75 !important;
            color: white !important;
            font-size: 1.1rem !important;
            padding: 1rem !important;
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 10px 20px rgba(14, 78, 117, 0.2);
            transition: all 0.3s ease;
        }}
        .stButton button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(14, 78, 117, 0.3);
        }}
        
        /* Hide streamlit default elements */
        #MainMenu, footer, header {{visibility: hidden;}}
        
        /* Custom Upload Styling */
        .upload-header {{
            font-family: 'Outfit', sans-serif;
            color: #0E4E75;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        </style>
    """, unsafe_allow_html=True)

def render_hero():
    # Profile Picture Loader
    img_tag = ""
    img_path = "assets/profile.png"
    if not os.path.exists(img_path):
        img_path = "assets/profile.jpg"
        
    if os.path.exists(img_path):
        img_b64 = get_img_as_base64(img_path)
        img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 140px; height: 140px; border-radius: 50%; border: 4px solid white; box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin-bottom: 1.5rem;">'
    else:
        img_tag = '<div style="font-size: 4rem;">👨‍⚕️</div>'

    # Render HTML Hero Banner
    st.markdown(f"""
        <div class="hero-cont">
            {img_tag}
            <h1>Dr. Rodrigo Gomes</h1>
            <div class="subtitle">ANTIGRAVITY CLINICAL AI</div>
        </div>
    """, unsafe_allow_html=True)

def render_metrics(num, audio):
    pass
