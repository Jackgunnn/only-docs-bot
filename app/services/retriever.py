from app.core.config import MAX_FULL_DOC_CHUNKS


def store_chunks(
    collection,
    chunks: list[str],
    embeddings: list,
    session_id: str,
    filename: str,
) -> None:
    """Store chunks and embeddings into a ChromaDB collection."""
    ids = [f"{session_id}_{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "session_id": session_id} for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def get_uploaded_sources(collection) -> set[str]:
    """Return set of filenames already uploaded in this session."""
    if collection.count() == 0:
        return set()
    results = collection.get(include=["metadatas"])
    return {m.get("source", "") for m in results["metadatas"]}


def retrieve_docs(
    collection,
    query_embedding: list,
    full_doc: bool,
    n_results: int = 5,
) -> list[str]:
    """Retrieve relevant chunks — all chunks if full_doc, else semantic search."""
    if full_doc:
        all_docs = collection.get()
        docs = all_docs["documents"][:MAX_FULL_DOC_CHUNKS]
        print(f"[FULL DOC MODE] Using {len(docs)} chunks")
    else:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )
        docs = results["documents"][0]
        print(f"[PARTIAL MODE] Using {len(docs)} chunks")

    return docs
