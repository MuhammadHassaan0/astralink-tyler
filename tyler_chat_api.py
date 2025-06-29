simport os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

from fastapi.middleware.cors import CORSMiddleware

# Load your OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Please set OPENAI_API_KEY as an env var.")

app = FastAPI()


# ─── ENABLE CORS ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astralink.life"],   # ← your front-end origin
    allow_methods=["POST", "OPTIONS"],          # only these HTTP verbs
    allow_headers=["*"],                        # allow all headers
)
# ────────────────────────────────────────────────────────────

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

# … imports, CORS, SYSTEM_PROMPT, ChatRequest …



# ← Moved health check here, *after* chat()
@app.get("/healthz")
async def healthz():
    """
    Health check for Render (or any load-balancer):
    Returns HTTP 200 {"status":"ok"} so they know the service is up.
    """
    return {"status": "ok"}
@app.post("/chat")

async def chat(payload: ChatRequest):
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": payload.message}

        ]
        resp = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,
    max_tokens=150,
)

        return {"reply": resp.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
