# webapp/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/", StaticFiles(directory="webapp", html=True), name="static")

@app.get("/health")
async def health():
    return {"status": "ok"}
