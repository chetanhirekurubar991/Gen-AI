#Step 1 — Connect to Your Existing ChromaDB Collection
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
client=chromadb.PersistentClient(path='/Users/chetanhirekurubar/Desktop/RagProjectDB') # 'Client' just for testing use 'PersistentClient'
collection=client.get_collection(name='chetan') # use instead of 'get_collection' to 'get_or_create_collection'
# print(collection.count())
model=SentenceTransformer('all-MiniLM-L6-v2')

#Step 2 — Convert User Query into Embedding
# query='which is popular programming language'
# query_embedding=model.encode([query])
# print(query_embedding[0])

#Step 3 — Perform Top-K Similarity Search + Print Scores & Step 4 — Experiment with Different K Values
# for k in [3]: # in that array use any number it's less than number of chunks like [2,4,6]
#     results=collection.query(
#         query_embeddings=query_embedding.tolist(),
#         n_results=k,
#         include=['documents','distances','embeddings']
#     )
#     for i ,(doc,score) in enumerate(zip(results['documents'][0],results['distances'][0])):
#         similarity=1-score
#         print(f"Top-K : {k} Rank : {i+1} similarity : {similarity:.4f} Text : {doc}")

#Step 5 — Implement MMR Retrieval
def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b))
def mmr(query_embedding,chunk_embeddings,chunks,k=3,lambda_val=0.7):
    selected=[]
    selected_embeddings=[]
    candidates=list(range((len(chunks))))
    for _ in range(k):
        mmr_score=[]
        for idx in candidates:
            relevance=cosine_similarity(query_embedding,chunk_embeddings[idx])
            if selected_embeddings:
                redundancy=max(cosine_similarity(chunk_embeddings[idx],s)for s in selected_embeddings)
            else:
                redundancy=0
            score=lambda_val*relevance-(1-lambda_val)*redundancy
            mmr_score.append((idx,score))
        best_idx=max(mmr_score,key=lambda x:x[1])[0]
        selected.append(chunks[best_idx])
        selected_embeddings.append(chunk_embeddings[best_idx])
        candidates.remove(best_idx)
    return selected

#Step 6 — Compare Similarity vs MMR Results
# print(f"{'='*5} SIMILARITY TOP 3 {'='*5}")
# for i, (doc,score) in enumerate(zip(results['documents'][0],results['distances'][0])):
#     print(f"Rank {i+1} | Score : {score:.4f} | {doc[:100]}")
# chunks=results["documents"][0]
# chunk_embeddings=results["embeddings"][0]
# mmr_results=mmr(query_embedding[0],chunk_embeddings,chunks)
# print(f"{'='*5} MMR TOP 5 {'='*5}")
# for i,doc in enumerate(mmr_results):
#     print(f"Rank : {i+1} | {doc[:100]}")

#Step 7 — Prepare Final Context for LLM Prompt
# context="\n\n".join(mmr_results)
# prompt=f"""
# You are helpful assistant.Answer only using this context below.
# Context:{context}
# Question:{query}
# Answer:
# """
# print(prompt)

#Step 8 — Final Clean Pipeline End to End
def rag_pipeline(query,client_collection,embedding_model,k=3,lambda_val=0.7):
    query_embedding=embedding_model.encode([query])[0]
    results=client_collection.query(
        query_embeddings=query_embedding,
        n_results=4,
        include=['documents','distances','embeddings']
    )
    chunks=results['documents'][0]
    chunk_embeddings=results['embeddings'][0]
    mmr_chunks=mmr(query_embedding,chunk_embeddings,chunks,k=k,lambda_val=lambda_val)
    context="\n\n".join(mmr_chunks)
    prompt=f"""
    You are a helpful assistant. Answer only using this below context.
    Context:{context}
    Question:{query}
    Answer :"""
    return prompt
print(rag_pipeline("which is popular programming language",collection,model))