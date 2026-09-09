import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="BIS AI Portal | SIH 2026", layout="wide", page_icon="🏛️")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(165deg, #022a40 0%, #061c2e 30%, #161a24 60%, #4a2522 100%) !important;
        font-family: 'Segoe UI', 'Poppins', sans-serif;
        color: white;
    }
    [data-testid="stHeader"] { background: transparent; }
    
    .stTextInput > div > div > input {
        background: rgba(30, 34, 43, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 15px 20px !important;
    }
    
    .stMarkdown div p {
        background: rgba(30, 34, 43, 0.7);
        padding: 15px 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #e2e4e9;
        font-size: 14px;
        line-height: 1.6;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- GEMINI SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.warning("⚠️ API Key not found in Streamlit Secrets.")

# --- MAIN UI ---
st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 28px; font-weight: 500;'>Good afternoon</h1><h2 style='font-size: 32px; font-weight: 600; margin-bottom: 40px;'>What can I help you with today?</h2></div>", unsafe_allow_html=True)

user_query = st.text_input("Ask anything", placeholder="Type your query...")

# --- CHAT LOGIC ---
if user_query:
    st.write("🏛️ Engine Processing...")
    
    system_instruction = (
        "You are the National BIS Assistant for SIH 2026, an official AI for Indian compliance. "
        "Keep answers professional, accurate, and format them beautifully using Markdown. "
        "If a user asks about standards (like cement, gold, toys), provide the relevant IS rules. "
        "Do not hallucinate fake laws."
    )
    
    try:
        full_prompt = f"{system_instruction}\n\nUser Question: {user_query}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
    except Exception as e:
        st.error(f"**Backend Error:** API request failed. Details: {str(e)}")
