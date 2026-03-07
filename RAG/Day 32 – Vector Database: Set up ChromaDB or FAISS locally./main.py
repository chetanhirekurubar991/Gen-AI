import chromadb
from sentence_transformers import SentenceTransformer
model=SentenceTransformer('all-MiniLM-L6-v2')
# print("chromadb version : ",chromadb.__version__)
# print("sentence_transformers version: ",model.__version__)

# Test
# test_embedding=model.encode('Hello World')
# print("Embedding Shape",test_embedding.shape)

documents = [
    "Python is a popular programming language for data science.",
    "ChromaDB is a vector database used for similarity search.",
    "Machine learning models learn patterns from data.",
    "Sentence transformers convert text into numerical embeddings.",
    "RAG stands for Retrieval Augmented Generation."
]
# print("Total Doc : ",len(documents))

client=chromadb.PersistentClient(path='/Users/chetanhirekurubar/Desktop/RagProjectDB')
collection=client.create_collection(name='chetan')
# print("Collection is : ",collection.name)

embedding=model.encode(documents)
collection.add(
    ids=["doc1","doc2","doc3","doc4","doc5"],
    embeddings=embedding.tolist(),
    documents=documents,
    metadatas=[
        {"source":"python_doc"},
        {"source":"chromadb_doc"},
        {"source":"ml_doc"},
        {"source":"nlp_doc"},
        {"source":"rag_doc"}
    ]
)
# print("Documented Inserted",collection.count())

query="What is vector databases?"
query_embedding=model.encode(query).tolist()
result=collection.query(
    query_embeddings=query_embedding,
    n_results=3
)
# print(result)

print("Query : ",query)
for i in range(len(result['documents'][0])):
    print("Document : ",result['documents'][0][i])
    print("Metadata : ",result['metadatas'][0][i])
    print("Distance : ",result['distances'][0][i])