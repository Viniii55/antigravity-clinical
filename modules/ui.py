import streamlit as st
import os

def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@400;600;700&display=swap');
        
        /* --- GLOBAL THEME --- */
        html, body, [class*="css"] {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #262730;
        }
        
        /* --- HEADERS --- */
        h1, h2, h3 {
            color: #0E4E75 !important;
            font-weight: 700;
        }
        
        /* --- BUTTONS --- */
        div.stButton > button {
            background-color: #0E4E75;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(14, 78, 117, 0.2);
        }
        div.stButton > button:hover {
            background-color: #09344f;
            box-shadow: 0 6px 8px rgba(14, 78, 117, 0.3);
            transform: translateY(-2px);
        }
        
        /* --- FILE UPLOADER --- */
        .stFileUploader {
            border: 1px dashed #0E4E75;
            border-radius: 10px;
            padding: 1rem;
            background-color: #F8FAFC;
        }

        /* --- TEXT AREA (REPORT) --- */
        .stTextArea textarea {
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            font-size: 16px;
            line-height: 1.6;
            padding: 15px;
        }
        
        /* --- HIDE DEFAULT STREAMLIT ELEMENTS --- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* --- CARDS & CONTAINERS --- */
        .clinical-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_hero():
    # Container Principal do Hero
    st.markdown("""
    <div style="padding: 1rem 0 2rem 0; border-bottom: 2px solid #F0F2F6; margin-bottom: 2rem;">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 5], gap="medium")
    
    with col1:
        # Profile Picture Logic
        img_path = "assets/profile.png"
        if not os.path.exists(img_path):
            img_path = "assets/profile.jpg"
            
        if os.path.exists(img_path):
            st.image(img_path, width=150) # Aumentando para 150px
        else:
            st.markdown("""
                <div style='
                    width: 150px; height: 150px; 
                    background: #0E4E75; 
                    border-radius: 12px; display: flex; align-items: center; justify-content: center;
                    color: white; font-size: 4rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    👨‍⚕️
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='display: flex; flex-direction: column; justify-content: center; height: 100%; padding-top: 20px;'>
                <h1 style='
                    color: #0E4E75;
                    font-size: 2.8rem; 
                    margin: 0;
                    line-height: 1.1;
                    font-family: "Helvetica Neue", sans-serif;
                '>Antigravity Clinical AI <span style='font-weight: 300; color: #94A3B8;'>|</span> Dr. Rodrigo Gomes</h1>
                <p style='
                    color: #64748B; 
                    font-size: 1.2rem; 
                    margin-top: 10px;
                    font-weight: 400;
                    font-family: "Helvetica Neue", sans-serif;
                '>
                    Transformando anotações brutas em laudos clínicos estruturados.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_metrics(num_images, has_audio):
    # Simplified metrics for clean look or empty pass if not needed in new design
    pass
