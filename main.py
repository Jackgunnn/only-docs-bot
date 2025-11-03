import data_pipeline, chunk_embed_store

print("Loading Data...\n")
data_pipeline.load_data()

print("\nCleaning Data...\n")
data_pipeline.clean_data()

print("\nChunking Data...\n")
chunks = chunk_embed_store.chunk_data()

print("\nCreating Embeddings...\n")
embeddings = chunk_embed_store.emded_data(chunks)

print("\nStoring Data...\n")
chunk_embed_store.store_data(chunks, embeddings)