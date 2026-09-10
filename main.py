import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import google.generativeai as genai

# Gemini API Key Render ke Environment Variables se uthayega (Secure)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Tera exact model locked
MODEL_NAME = 'gemini-3.6-flash'
model = genai.GenerativeModel(MODEL_NAME)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tera original index.html serve karega
@app.get("/", response_class=HTMLResponse)
async def get_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: index.html not found in repository!</h1>"

# Chat endpoint with SIH compliance prompt
@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    system_instruction = (
        "You are the National BIS Assistant for SIH 2026, an official AI for Indian compliance. "
        "Keep answers professional, accurate, and format them beautifully using Markdown. "
        "If a user asks about standards (like cement, gold, toys), provide the relevant IS rules. "
        "Do not hallucinate fake laws."
    )
    
    try:
        full_prompt = f"{system_instruction}\n\nUser Query: {user_message}"
        response = model.generate_content(full_prompt)
        return JSONResponse({"reply": response.text})
    except Exception as e:
        return JSONResponse({"reply": f"**Backend Error:** {str(e)}"})
