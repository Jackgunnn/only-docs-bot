from sentence_transformers import SentenceTransformer
import chromadb
import ollama

# Initialize DB + embeddings
client = chromadb.PersistentClient(path="./chroma_db")
model = SentenceTransformer("all-MiniLM-L6-v2")

def answer_query(query):
    query_embedding = model.encode(query).tolist()
    collection = client.get_or_create_collection(name="docker_docs")

    # Retrieve best matches
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results["documents"][0]
    context = "\n\n".join(documents)

    print("\n🔍 Query:", query)
    print("\n📄 Retrieved Context:")
    for i, doc in enumerate(documents, start=1):
        print(f"\n--- Result #{i} ---\n{doc[:300]}...\n")

    # Build prompt
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

    # Call Ollama (llama3)
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    print("\n✅ Final Answer:")
    print(response["message"]["content"])


if __name__ == "__main__":
    user_query = input("\nEnter query: ")
    answer_query(user_query)
