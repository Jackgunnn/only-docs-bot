import time
import uuid

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response

from app.core.config import MAX_PDF_SIZE_MB, MAX_PDFS_PER_SESSION
from app.models.schemas import AskRequest, AskResponse, UploadResponse, SessionResponse, CleanupResponse
from app.services.pdf import extract_text, chunk_text
from app.services.llm import needs_full_document, generate_response, build_prompt
from app.services.retriever import store_chunks, get_uploaded_sources, retrieve_docs
from app.dependencies import get_embed_model, get_chroma_client

router = APIRouter()


@router.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


@router.post("/session", response_model=SessionResponse)
def create_session():
    session_id = str(uuid.uuid4())
    print(f"[SESSION] Created: {session_id}")
    return SessionResponse(session_id=session_id)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(session_id: str, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    chroma_client = get_chroma_client()
    collection = chroma_client.get_or_create_collection(f"session_{session_id}")

    sources = get_uploaded_sources(collection)
    if len(sources) >= MAX_PDFS_PER_SESSION:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {MAX_PDFS_PER_SESSION} PDFs allowed per session."
        )

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_PDF_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_PDF_SIZE_MB}MB."
        )

    try:
        text = extract_text(contents)
        if not text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text. PDF may be scanned or image-based."
            )

        chunks = chunk_text(text)
        embed_model = get_embed_model()
        embeddings = embed_model.encode(chunks).tolist()

        store_chunks(collection, chunks, embeddings, session_id, file.filename)

        print(f"[UPLOAD] Session {session_id}: {file.filename} — {len(chunks)} chunks stored")
        return UploadResponse(
            message=f"PDF '{file.filename}' uploaded successfully.",
            chunks_stored=len(chunks)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=AskResponse)
def ask(data: AskRequest):
    try:
        chroma_client = get_chroma_client()
        collection = chroma_client.get_or_create_collection(f"session_{data.session_id}")

        if collection.count() == 0:
            return AskResponse(
                query=data.query,
                response="Please upload a PDF first before asking questions.",
                retrieved_docs_count=0
            )

        t0 = time.time()
        embed_model = get_embed_model()
        query_embedding = embed_model.encode(data.query).tolist()
        print(f"[TIMING] Embedding: {time.time() - t0:.2f}s")

        t1 = time.time()
        full_doc = needs_full_document(data.query)
        docs = retrieve_docs(collection, query_embedding, full_doc)
        print(f"[TIMING] Retrieval: {time.time() - t1:.2f}s")

        t2 = time.time()
        context = "\n\n".join(docs)
        prompt = build_prompt(context, data.query)
        max_tokens = 500 if full_doc else 400
        response = generate_response(prompt, max_tokens=max_tokens)
        print(f"[TIMING] LLM: {time.time() - t2:.2f}s")

        return AskResponse(
            query=data.query,
            response=response,
            retrieved_docs_count=len(docs)
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] /ask failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup/{session_id}", response_model=CleanupResponse)
def cleanup_session(session_id: str):
    try:
        chroma_client = get_chroma_client()
        try:
            chroma_client.delete_collection(f"session_{session_id}")
            print(f"[CLEANUP] Deleted collection for session {session_id}")
        except Exception:
            pass
        return CleanupResponse(message="Session cleaned up successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
