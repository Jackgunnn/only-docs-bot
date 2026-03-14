from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router
from app.dependencies import get_embed_model, get_chroma_client

app = FastAPI(
    title="Only Docs Bot",
    description="RAG-based PDF Q&A chatbot",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return FileResponse("static/chat.html")


@app.on_event("startup")
async def startup_event():
    """Pre-load heavy models at startup so first request is fast."""
    print("[STARTUP] Loading models...")
    get_embed_model()
    get_chroma_client()
    print("[STARTUP] Ready!")
