from fastapi import FastAPI

app = FastAPI()

@app.get("/api/healthz")
async def healthz():
    """
    Health check for Vercel (or any host).
    Returns HTTP 200 {"status": "ok"} so they know the service is up.
    """
    return {"status": "ok"}

