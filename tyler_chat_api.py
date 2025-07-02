import os 
import base64
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware

# ── Load keys from environment ───────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID       = os.getenv("ELEVEN_VOICE_ID")

if not openai.api_key or not ELEVEN_API_KEY or not VOICE_ID:
    raise RuntimeError("Set OPENAI_API_KEY, ELEVEN_API_KEY & ELEVEN_VOICE_ID env vars")

# ── FastAPI setup ────────────────────────────────────────────
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astralink.life"],  # or "*" while testing
    allow_methods=["POST","OPTIONS"],
    allow_headers=["*"],
)

# ── System prompt with coaching context ───────────────────────
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

async def text_to_speech(text: str) -> str:
    """
    Calls Eleven Labs Text-to-Speech API,
    returns a base64-encoded mp3 data URI.
    """
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

    b64 = base64.b64encode(mp3_bytes).decode()
    return f"data:audio/mpeg;base64,{b64}"

@app.post("/chat")
async def chat(payload: ChatRequest):
    # 1️⃣ Get Tyler’s text via OpenAI
    messages = [
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user",   "content": payload.message}
    ]
    try:
        gpt = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        reply = gpt.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(500, f"OpenAI error: {e}")

    # 2️⃣ Generate audio
    try:
        audio_uri = await text_to_speech(reply)
    except Exception as e:
        # If TTS fails, return null for audio
        audio_uri = None

    return {"reply": reply, "audio": audio_uri}

@app.get("/healthz")
async def healthz():
    return {"status":"ok"}
mport os
import base64
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware

# ─── Load your keys from env vars ─────────────────────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID       = os.getenv("ELEVEN_VOICE_ID")

if not openai.api_key or not ELEVEN_API_KEY or not VOICE_ID:
    raise RuntimeError(
        "Please set OPENAI_API_KEY, ELEVEN_API_KEY & ELEVEN_VOICE_ID env vars"
    )

# ─── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astralink.life"],  # your front‐end origin
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# ─── Tyler’s system prompt ────────────────────────────────────────────────────
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

# ─── ElevenLabs TTS helper ────────────────────────────────────────────────────
async def text_to_speech(text: str) -> str:
    """
    Calls Eleven Labs TTS API and returns a base64‐encoded MP3 data URI.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        mp3_bytes = resp.content

    b64 = base64.b64encode(mp3_bytes).decode()
    return f"data:audio/mpeg;base64,{b64}"

# ─── Chat endpoint ───────────────────────────────────────────────────────────
@app.post("/chat")
async def chat(payload: ChatRequest):
    # 1) Generate Tyler-style reply
    try:
        gpt_resp = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": payload.message}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        reply = gpt_resp.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(500, f"OpenAI error: {e}")

    # 2) Synthesize voice
    audio_uri = None
    try:
        audio_uri = await text_to_speech(reply)
    except Exception:
        # fallback to text‐only if TTS fails
        audio_uri = None

    return {"reply": reply, "audio": audio_uri}

# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/healthz")
async def healthz():
    """
    For load-balancers or uptime checks.
    """
    return {"status": "ok"}

