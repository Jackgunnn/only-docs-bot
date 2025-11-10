from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
from main import *
from configurations import EMBED_MODEL, DOCKER_COLLECS


app = FastAPI()


# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    query_embedding = EMBED_MODEL.encode(query).tolist()

    # 2️⃣ Retrieve similar docs
    results = DOCKER_COLLECS.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = results["documents"][0]
    context = "\n\n".join(docs)

    # 3️⃣ Build prompt
    prompt = f"""
        Please answer the query using only the provided context. 
        If the question goes beyond your current knowledge of Docker, respond with:
        “I have limited knowledge of Docker, and this is beyond my current scope. 
        I’m still being trained and tested — sorry for the inconvenience." If the question
        is inappropriate, respond with: "Fuck You!!!"

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
