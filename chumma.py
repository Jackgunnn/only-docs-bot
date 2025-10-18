import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    ids=["id1", "id2", "id3"],
    documents=[
        "Collections are where you'll store your embeddings, documents, and any additional metadata. "
        "Collections index your embeddings and documents, and enable efficient retrieval and filtering. ",
        "Ephemeral client starts a Chroma server in-memory, so any data you ingest will be lost when your program terminates.",
        "Persistent client is used if you need data persistence, so any data you ingest will not be lost when your program terminates."
    ]
)

results = collection.query(
    query_texts=["What"], # Chroma will embed this for you
    n_results=1 # how many results to return
)
print(results["documents"])
print(results["distances"])
