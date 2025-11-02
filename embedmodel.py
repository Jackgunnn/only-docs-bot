from sentence_transformers import SentenceTransformer
sentences = ["T", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# embeddings = model.encode(sentences[0])
# print(embeddings)
print(model.get_max_seq_length())
