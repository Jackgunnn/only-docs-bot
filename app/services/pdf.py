import io
import pypdf
from app.core.config import CHUNK_SIZE


def extract_text(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes in memory — no disk save."""
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def chunk_text(text: str, max_length: int = CHUNK_SIZE) -> list[str]:
    """Split text into chunks of max_length words."""
    words = text.split()
    return [
        " ".join(words[i:i + max_length])
        for i in range(0, len(words), max_length)
    ]
