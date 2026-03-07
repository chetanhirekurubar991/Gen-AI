import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path='/Users/chetanhirekurubar/Desktop/RagProjectDB')  # same path as before

collection = client.get_collection(name='chetan')  # same collection name

print("Documents in DB:", collection.count())

query = "How do embeddings work?"
query_embedding = model.encode(query).tolist()

results = collection.query(query_embeddings=query_embedding, n_results=3)

for i in range(len(results["documents"][0])):
    print(f"Rank {i+1} | {results['documents'][0][i]} | Distance: {results['distances'][0][i]:.4f}")