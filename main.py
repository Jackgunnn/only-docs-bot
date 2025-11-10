import os
import re
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from configurations import RAW_DIR, RAW_DATA, CLEANED_DATA, EMBED_MODEL, DOCKER_COLLECS

def load_data(docs_dir=RAW_DIR, output_file=RAW_DATA):
    """
    Loads all markdown (.md) files from a directory and
    combines their content into a single text file.

    Args:
        docs_dir (str): Directory to search for markdown files.
        output_file (str): Path to save the combined text.
    """

    markdown_files = []

    # Collect all .md file paths
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))

    # Write all contents into one file
    i = 1
    with open(output_file, "w", encoding="utf-8") as out:
        for md_path in markdown_files:
            print(i, md_path)
            with open(md_path, "r", encoding="utf-8") as f:
                file_content = f.read()
                out.write(f"## FILE: {md_path}\n\n{file_content}\n\n")
            i+=1

    print(f"Saved {len(markdown_files)} markdown files to {output_file}")


def clean_data(input_file=RAW_DATA, output_file=CLEANED_DATA):
    """
    Cleans the raw data file and saves the cleaned data 
    into a single text file.

    Args:
        input_file (str): Directory to search for markdown files.
        output_file (str): Path to save the combined text.  
    """

    # --- Read raw file ---
    with open(input_file, "r", encoding="utf-8") as f:
        raw = f.read()

    # Remove HTML tags
    soup = BeautifulSoup(raw, "html.parser")
    raw = soup.get_text()

    # Remove YAML front matter
    raw = re.sub(r"^---[\s\S]*?---\s*", "", raw, flags=re.MULTILINE)

    # Remove markdown formatting symbols
    raw = re.sub(r"[#*_>\[\]{}~=]+", " ", raw)

    # Remove markdown list bullets
    raw = re.sub(r"(?m)^\s*(?:[-*]|\d+[.)])\s+", "", raw)

    # Keep only readable chars (letters, digits, punctuation, links)
    raw = re.sub(r"[^A-Za-z0-9:/._\-\s\n!?]", " ", raw)

    # Normalize all existing line breaks to spaces
    raw = re.sub(r"\n+", " ", raw)
    raw = re.sub(r"[ \t]+", " ", raw).strip()

    # Split sentences → remove punctuation → newline
    raw = re.sub(r'[.!?]\s+(?=[A-Z0-9])', r'\n', raw)

    # --- Save to a new text file ---
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(raw)

    print(f"Cleaned Data saved to {output_file}")


def chunk_data(input_file = CLEANED_DATA, max_length=200):

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
    embeddings = [EMBED_MODEL.encode(chunk) for chunk in chunks]
    print("Embeddings created successfully!")
    return embeddings
    

def store_data(chunks, embeddings):
    
    DOCKER_COLLECS.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings
    )

    print("Stored all chunks + embeddings in ChromaDB!")


if __name__ == "__main__":
    print("Loading Data...\n")
    load_data()

    print("\nCleaning Data...\n")
    clean_data()

    print("\nChunking Data...\n")
    chunks = chunk_data()

    print("\nCreating Embeddings...\n")
    embeddings = emded_data(chunks)

    print("\nStoring Data...\n")
    store_data(chunks, embeddings)