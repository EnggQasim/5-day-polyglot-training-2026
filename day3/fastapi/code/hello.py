"""
The smallest possible FastAPI app.

Run (from this folder):
    cd day3/fastapi/code
    uvicorn hello:app --reload --port 8000

Then open http://localhost:8000/docs
"""
from fastapi import FastAPI

app = FastAPI(title="Pixel Quest API - hello")


@app.get("/")
def root():
    return {"message": "Welcome to Pixel Quest"}


@app.get("/health")
def health():
    return {"status": "ok"}
