import requests
from app.core.config import (
    GROQ_API_KEY,
    GROQ_URL,
    GROQ_MODELS,
    GROQ_DECISION_MODEL,
)


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }


def needs_full_document(query: str) -> bool:
    """Ask a fast LLM whether this query needs the full document or just parts."""
    if not GROQ_API_KEY:
        return False

    data = {
        "model": GROQ_DECISION_MODEL,
        "messages": [{
            "role": "user",
            "content": (
                f'Does this query require reading the full document or just specific parts?\n'
                f'Query: "{query}"\n'
                f'Reply with only one word: FULL or PARTIAL'
            )
        }],
        "max_tokens": 5,
    }

    try:
        response = requests.post(GROQ_URL, headers=_headers(), json=data)
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"].strip().upper()
            print(f"[LLM DECISION] {answer}")
            return "FULL" in answer
    except Exception as e:
        print(f"[LLM DECISION ERROR] {e}")

    return False


def generate_response(prompt: str, max_tokens: int = 500) -> str:
    """Generate a response using Groq API with model fallback."""
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY is not set.")

    for model in GROQ_MODELS:
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        response = requests.post(GROQ_URL, headers=_headers(), json=data)
        if response.status_code == 200:
            print(f"[MODEL USED] {model}")
            return response.json()["choices"][0]["message"]["content"]
        print(f"[RETRY] {model} failed ({response.status_code}), trying next...")

    raise Exception("All models failed. Please try again later.")


def build_prompt(context: str, query: str) -> str:
    return f"""You are a helpful assistant. Use the context below to answer questions clearly and in detail.
You may give thoughtful analysis, summaries, and opinions based strictly on what is in the context.
If there is truly nothing relevant in the context, say "I don't have enough information about that."

Context:
{context}

Question:
{query}

Answer:"""
