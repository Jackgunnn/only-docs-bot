from sentence_transformers import SentenceTransformer
import chromadb

def chunk_data(input_file = "data/cleaned_data.txt", max_length=200):

    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()

    words = data.split()
    chunks = []
    for i in range(0, len(words), max_length):
        chunks.append(" ".join(words[i:i+max_length]))

    # with open("data/chunks.txt", "w", encoding="utf-8") as f:
    #     f.write(str(chunks))

    print("Chunks created successfully!")
    return chunks


def emded_data(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = [model.encode(chunk) for chunk in chunks]
    print("Embeddings created successfully!")
    return embeddings
    

def store_data(chunks, embeddings):
    client = chromadb.PersistentClient(path="./chroma_db")

    collection = client.get_or_create_collection(name="docker_docs")

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings
    )

    print("Stored all chunks + embeddings in ChromaDB!")
