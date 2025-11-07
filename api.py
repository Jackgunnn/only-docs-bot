from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import subprocess

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading Embedding Model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docker_docs")
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from sentence_transformers import SentenceTransformer
import subprocess

# ✅ Initialize
app = FastAPI()

# ✅ Allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docker_docs")

# ✅ Request body
class AskRequest(BaseModel):
    query: str

# ✅ Call Ollama
def generate_llm_response(prompt: str):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        output = result.stdout.decode("utf-8")
    except:
        output = result.stdout.decode("utf-8", errors="ignore")

    return output.strip()


# ✅ API endpoint
@app.post("/ask")
def ask(data: AskRequest):
    query = data.query

    # 1️⃣ Embed query
    query_embedding = embed_model.encode(query).tolist()

    # 2️⃣ Retrieve similar docs
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = results["documents"][0]
    context = "\n\n".join(docs)

    # 3️⃣ Build prompt
    prompt = f"""
You are a helpful assistant. 
Answer **only** from the provided context. 
If context does not contain the answer, say "Not found in context."
Context:
{context}

Question:
{query}

Answer:
"""

    # 4️⃣ Pass to LLM
    response = generate_llm_response(prompt)

    return {
        "query": query,
        "response": response,
        "retrieved_docs_count": len(docs)
    }
