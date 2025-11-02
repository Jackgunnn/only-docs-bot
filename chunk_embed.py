from sentence_transformers import SentenceTransformer

def chunk_data(input_file = "data/cleaned_data.txt", max_length=200):
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()

    words = data.split()
    chunks = []
    for i in range(0, len(words), max_length):
        chunks.append(" ".join(words[i:i+max_length]))

    # with open("data/chunks.txt", "w", encoding="utf-8") as f:
    #     f.write(str(chunks))

    return chunks

chunks = chunk_data()
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = [model.encode(chunk) for chunk in chunks]

print(embeddings)