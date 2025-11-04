from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import json

# ✅ Initialize
app = FastAPI()

# ✅ Load embedding model once
print("Loading Embedding Model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docker_docs")


# ✅ Request body
class AskRequest(BaseModel):
    query: str
    top_k: int = 3


# ✅ Call Ollama safely
def generate_llm_response(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout.strip()
    except Exception as e:
        return f"LLM error: {str(e)}"


# ✅ API endpoint
@app.post("/ask")
def ask(data: AskRequest):
    query = data.query
    top_k = data.top_k

    try:
        # 1️⃣ Create embedding
        query_embedding = embed_model.encode(query).tolist()

        # 2️⃣ Retrieve similar docs
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        docs = results.get("documents", [[]])[0]

        if not docs:
            return {
                "query": query,
                "response": "No relevant documents found.",
                "retrieved_docs_count": 0
            }

        # ✅ Join top docs as context
        context = "\n\n====\n\n".join(docs)

        # 3️⃣ Build structured prompt
        prompt = f"""
Use ONLY the context below to answer the question.
If answer is unknown, say "Not found in documentation".

Context:
{context}

Question:
{query}

Answer:
"""

        # 4️⃣ LLM
        response = generate_llm_response(prompt)

        return {
            "query": query,
            "response": response,
            "retrieved_docs_count": len(docs),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Optional home route
@app.get("/")
def home():
    return {"message": "RAG API is running ✅"}
