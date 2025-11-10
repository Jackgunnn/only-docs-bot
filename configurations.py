from sentence_transformers import SentenceTransformer
import chromadb

# PATHS
RAW_DIR = "./raw_content"
RAW_DATA = "./data/raw_data.txt"
CLEANED_DATA = "./data/cleaned_data.txt" 
CHROMA_DIR = "./chroma_db"

# MODEL
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB
CHROMA_CLIENT = chromadb.PersistentClient(path= CHROMA_DIR)
DOCKER_COLLECS = CHROMA_CLIENT.get_or_create_collection("docker_docs")

