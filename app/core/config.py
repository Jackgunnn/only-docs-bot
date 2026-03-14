import os
from dotenv import load_dotenv

load_dotenv()

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]
GROQ_DECISION_MODEL = "llama-3.1-8b-instant"

# PDF limits
MAX_PDF_SIZE_MB = 10
MAX_PDFS_PER_SESSION = 2

# Chunking
CHUNK_SIZE = 300  # words per chunk
MAX_FULL_DOC_CHUNKS = 10

# Embedding model
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
