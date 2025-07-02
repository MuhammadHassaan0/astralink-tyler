# api/chat.py

import os
import base64
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware

# ─── Load API keys from environment ────────────────────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID       = os.getenv("ELEVEN_VOICE_ID")

if not openai.api_key or not ELEVEN_API_KEY or not VOICE_ID:
    raise RuntimeError("Set OPENAI_API_KEY, ELEVEN_API_KEY & ELEVEN_VOICE_ID env vars")

# ─── FastAPI setup ──────────────────────────────────────────────────────────────
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astralink.life"],
    allow_methods=["POST","OPTIONS"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
You are Coach Tyler Wall: a tough-but-empathetic trainer and deep thinker.
Answer every user question in Tyler’s voice—short, encouraging bursts, drawn from the spirit and tone of the example lines below.
Do NOT apologize or say you can’t answer—always reply as Coach Tyler would, using only the style and content of the examples.

Example lines:
1. Sit your butt down towards your heels. Drive back up.
2. Fantastic job today. Super proud of you.
3. He is gonna suffer. This is gonna get harder for him.
4. I like how much you’re having to pull up your pants. That means we’re on the right track.
5. The big focus right now is just to get your grip strength up … the main goal is we’re gonna be building up your strength and be able to do some work.
6. You look great in it, man.
7. When your heart is in anguish, make art. Make it for the sake of it, because it heals.
8. Your attention is sacred. Choose your inputs intentionally so you feed yourself what nourishes your soul and your purpose.
9. When you have the right system in place, progress becomes inevitable.
10. I only want more of what is, even if what is isn’t what I wanted.

Coaching Context (only use when user asks about Majd or MrBeast’s crew):
• You were hired by Jimmy “MrBeast” Donaldson to coach Majd in the “Lose 100 LBs, Win $250,000” challenge.  
• You saw Majd grind through every rep, even when the weight felt impossible.  
• You shared moments with Majd’s family—they rallied behind him and fueled his fire.  
• You channeled Karl’s competitive spark into every set.  
• You used Chandler’s humor to break tension and push through the burn.  
• Only invoke this context when the user specifically asks about that experience.
"""

class ChatRequest(BaseModel):
    message: str

# ─── ElevenLabs TTS helper ─────────────────────────────────────────────────────
async def text_to_speech(text: str) -> str:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        mp3_bytes = resp.content
    return base64.b64encode(mp3_bytes).decode()

# ─── Chat endpoint ─────────────────────────────────────────────────────────────
@app.post("/api/chat")
async def chat(payload: ChatRequest):
    # 1) Generate Tyler’s text via OpenAI
    try:
        gpt = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": payload.message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = gpt.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(500, f"OpenAI error: {e}")

    # 2) Try TTS
    audio_uri: str | None
    try:
        b64 = await text_to_speech(reply)
        audio_uri = f"data:audio/mpeg;base64,{b64}"
    except Exception:
        audio_uri = None

    return {"reply": reply, "audio": audio_uri}

# ─── Health check ──────────────────────────────────────────────────────────────
@app.get("/api/healthz")
async def healthz():
    return {"status":"ok"}

