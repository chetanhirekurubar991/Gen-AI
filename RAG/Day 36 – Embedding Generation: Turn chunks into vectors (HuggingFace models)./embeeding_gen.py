#Step 1: Install sentence-transformers & Step 2: Load the Embedding Model
from sentence_transformers import SentenceTransformer
import time
import chromadb
model=SentenceTransformer("all-MiniLM-L6-v2")

#Step 3: Generate Embedding for a Single_Chunk
# chunk='Ai called as artificial intelligence'
# embedding=model.encode(chunk)
# print(embedding.shape) #(384,)

#Step 4 & 5: Embed 5 Chunks + Batch Encode
chunks=["Large Language Models are neural networks trained on massive text datasets to understand and generate human-like language.",
    "LLMs use transformer architecture with self-attention to capture relationships between words in a sequence.",
    "Embeddings convert text into numerical vectors that represent semantic meaning for retrieval and similarity search.",
    "Retrieval Augmented Generation combines vector search with LLM reasoning to produce grounded responses.",
    "Fine-tuning adapts a pretrained language model to perform better on specific tasks or domains."
]
# start=time.time()
# embeddings=model.encode(chunks)
# stop=time.time()
# print(embeddings.shape,stop-start) #(5, 384)

start1=time.time()
batch_embeddings=model.encode(chunks,batch_size=2) #batch_size only controls how many are processed internally at once, not the output shape.
stop1=time.time()
print(batch_embeddings.shape,stop1-start1)

#Step 6 & 7: Measure Embedding Time + Integrate into ChromaDB
client=chromadb.Client()
collection=client.create_collection(name='rag_chunks')
embedding_list=batch_embeddings.tolist()
collection.upsert( # instead of 'add' use 'upsert' its helps to Adds if new or Updates if ID exists
    documents=chunks,
    embeddings=embedding_list,
    ids=["id1","id2","id3","id4","id5"]
)
print("Stored Successfully")

#Step 8: Verify Vector Dimension Consistency
query_embedding=model.encode("llm's are offline or online")
print(query_embedding.shape)
query_embeddings=query_embedding.tolist()
results=collection.query(
    query_embeddings=[query_embeddings],
    n_results=3
)
print(results['documents'])