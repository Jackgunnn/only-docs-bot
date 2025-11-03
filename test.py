from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
model = SentenceTransformer("all-MiniLM-L6-v2")
query = "What is a docker?"
query_embedding = model.encode(query).tolist()

collection = client.get_or_create_collection(name="docker_docs")

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\n🔍 Query:", query)
print("Top results:")
for i, doc in enumerate(results["documents"][0], start=1):
    print(f"{i}. {doc[:200]}...")