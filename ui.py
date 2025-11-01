import streamlit as st
import base64

def add_background(image_path: str):
    """Set full-screen background using a local image"""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: rgba(0,0,0,0);
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(10,10,10,0.85);
    }}
    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: #FFD700 !important; /* gold */
        font-family: 'Friz Quadrata', serif;
        text-shadow: 1px 1px 3px black;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
