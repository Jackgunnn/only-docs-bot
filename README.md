# Only Docs Bot

A RAG-based PDF Q&A chatbot. Upload a PDF and ask questions about it.

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **LLM:** Groq API (llama-3.3-70b-versatile with fallbacks)
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2
- **Vector DB:** ChromaDB
- **Frontend:** Vanilla HTML/CSS/JS

## Project Structure

```
only-docs-bot/
├── app/
│   ├── main.py              # FastAPI app + middleware
│   ├── dependencies.py      # Shared singletons (embed model, chroma)
│   ├── api/
│   │   └── routes.py        # All API endpoints
│   ├── services/
│   │   ├── llm.py           # Groq API logic + fallback
│   │   ├── pdf.py           # PDF extraction + chunking
│   │   └── retriever.py     # ChromaDB query logic
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response models
│   └── core/
│       └── config.py        # Environment variables + constants
├── static/
│   └── chat.html            # Frontend
├── docker/
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yml
├── requirements.txt
├── .env                     # Never committed
└── .gitignore
```

## Setup

### Local

```bash
# Clone the repo
git clone https://github.com/yuvabharathi12/only-docs-bot.git
cd only-docs-bot

# Create virtual environment
py -3.11 -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run
uvicorn app.main:app --reload
```

### Docker

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve frontend |
| POST | `/session` | Create new session |
| POST | `/upload?session_id=X` | Upload PDF |
| POST | `/ask` | Ask a question |
| POST | `/cleanup/{session_id}` | Delete session data |

## Deployment (EC2)

```bash
ssh -i "your-key.pem" ubuntu@your-ec2-ip
cd only-docs-bot
git pull
pip install -r requirements.txt
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &
disown
```
