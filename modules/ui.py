import streamlit as st
import base64
import os

def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

def load_custom_css():
    # Carregar imagem de fundo para o Banner
    header_bg = ""
    bg_path = "assets/hero.png"
    if not os.path.exists(bg_path):
        bg_path = "assets/hero.jpg"
    
    if os.path.exists(bg_path):
        img_b64 = get_img_as_base64(bg_path)
        header_bg = f"""
            background-image: linear-gradient(180deg, rgba(14, 78, 117, 0.9) 0%, rgba(14, 78, 117, 0.95) 100%), url("data:image/png;base64,{img_b64}");
            background-size: cover;
            background-position: center;
        """
    else:
        header_bg = "background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@400;600&display=swap');
        
        /* --- GLOBAL LAYOUT (Max Width 850px -> Mobile Friendly) --- */
        .block-container {{
            max-width: 850px !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }}
        
        /* --- HERO BANNER (Compact) --- */
        .hero-cont {{
            {header_bg}
            padding: 2rem 1rem 3rem 1rem;
            text-align: center;
            color: white;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 25px rgba(14, 78, 117, 0.15);
        }}
        
        /* --- TYPOGRAPHY --- */
        h1 {{
            font-family: 'Outfit', sans-serif;
            font-weight: 700 !important;
            font-size: 2.2rem !important;
            margin-bottom: 0.2rem !important;
            color: white !important;
        }}
        
        .subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            color: rgba(255,255,255,0.85);
            font-weight: 400;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        
        /* --- NATIVE CONTAINER STYLING --- */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important;
            border: 1px solid #E2E8F0 !important;
            background-color: white !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
            padding: 1.5rem !important;
        }}
        
        /* --- COMPONENT OVERRIDES --- */
        .stButton button {{
            width: 100%;
            background: #0E4E75 !important;
            color: white !important;
            font-size: 1rem !important;
            padding: 0.8rem !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }}
        .stButton button:hover {{
            background: #09344f !important;
            transform: scale(0.99);
        }}
        
        /* Hide streamlit default elements */
        #MainMenu, footer, header {{visibility: hidden;}}
        
        /* Custom Upload Styling */
        .upload-header {
            font-family: 'Outfit', sans-serif;
            color: #0E4E75;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0px;
        }

        /* --- MOBILE OPTIMIZATIONS --- */
        @media (max-width: 768px) {{
            /* Hide Sidebar completely on mobile for focus */
            section[data-testid="stSidebar"] {{
                display: none !important;
            }}
            /* Adjust padding for mobile */
            .hero-cont {{
                padding: 1.5rem 1rem 2rem 1rem !important;
            }}
            h1 {{
                font-size: 1.8rem !important;
            }}
        }}

        /* --- RESULT STATE STYLING --- */
        
        /* 1. Download Button (Green Success) */
        [data-testid="stDownloadButton"] button {{
            background-color: #2E7D32 !important;
            border: none !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 0.8rem 1.5rem !important;
            box-shadow: 0 4px 10px rgba(46, 125, 50, 0.3) !important;
        }}
        [data-testid="stDownloadButton"] button:hover {{
            background-color: #1B5E20 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(46, 125, 50, 0.4) !important;
        }}
        
        /* 2. Report Paper Look (Text Area) */
        .stTextArea textarea {{
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important; /* Elegant Shadow */
            border-radius: 12px !important;
            padding: 1.5rem !important;
            font-family: 'Helvetica Neue', Arial, sans-serif !important;
            line-height: 1.6 !important;
            color: #334155 !important;
        }}
        
        /* 3. Spinner/Loading Text */
        .stSpinner > div > div {{
            border-top-color: #0E4E75 !important;
        }}
        .stSpinner p {{
            color: #0E4E75 !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
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
        img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid white; margin-bottom: 1rem;">'
    else:
        img_tag = '<div style="font-size: 3rem; margin-bottom: 0.5rem;">👨‍⚕️</div>'

    # Render HTML Hero Banner (Compact)
    st.markdown(f"""
        <div class="hero-cont">
            {img_tag}
            <h1>Dr. Rodrigo Gomes</h1>
            <div class="subtitle">Antigravity Clinical AI</div>
        </div>
    """, unsafe_allow_html=True)

def render_metrics(num, audio):
    pass
