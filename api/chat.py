import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Load your OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Please set OPENAI_API_KEY as an env var.")

# Read your system prompt from an env var
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(payload: ChatRequest):
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": payload.message}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return {"reply": resp.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

