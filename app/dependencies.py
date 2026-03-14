from sentence_transformers import SentenceTransformer
import chromadb
from app.core.config import EMBED_MODEL_NAME

# Singletons — loaded once at startup
_embed_model = None
_chroma_client = None


def get_embed_model() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        print(f"[INIT] Loading embedding model: {EMBED_MODEL_NAME}")
        _embed_model = SentenceTransformer(EMBED_MODEL_NAME)
    return _embed_model


def get_chroma_client() -> chromadb.PersistentClient:
    global _chroma_client
    if _chroma_client is None:
        print("[INIT] Initializing ChromaDB client")
        _chroma_client = chromadb.PersistentClient(path="./chroma_db")
    return _chroma_client
