from pydantic import BaseModel, validator


class AskRequest(BaseModel):
    query: str
    session_id: str

    @validator("query")
    def query_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v[:1000]


class AskResponse(BaseModel):
    query: str
    response: str
    retrieved_docs_count: int


class UploadResponse(BaseModel):
    message: str
    chunks_stored: int


class SessionResponse(BaseModel):
    session_id: str


class CleanupResponse(BaseModel):
    message: str
