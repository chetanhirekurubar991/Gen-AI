from rank_bm25 import BM25Okapi
import numpy as np
import chromadb

#Step 1: Build Your BM25 Index
chunks = [
    "BM25 is a keyword based retrieval algorithm",
    "Semantic search uses vector embeddings for meaning",
    "Hybrid search combines BM25 and semantic search",
    "Chroma is a vector database for storing embeddings",
    "RAG systems retrieve documents before generating answers"
]
tokenized_chunks=[chunk.split() for chunk  in chunks]
bm25=BM25Okapi(tokenized_chunks)
# print("Total Doc Index :",len(tokenized_chunks))

#Step 2: Write a BM25 Search Function
def search_bm25(query,bm25):
    tokenized_query=query.split()
    scores=bm25.get_scores(tokenized_query)

    # Step 3: Return Top-K Results
    top_indexes=np.argsort(scores)[::-1][:2]
    # print(top_indexes)
    # print(scores)

    #Step 6: Add Scores to Each Result
    bm25_scores = {}
    for i in top_indexes:
        bm25_scores[chunks[i]]=scores[i]
    # print(bm25_scores)
    return [chunks[i] for i in top_indexes],bm25_scores

bm25_results=search_bm25('semantic search embeddings',bm25)
print('\nStep 6: Add Scores to Each Result')
print(bm25_results[1])

#Step 4: Connect Chroma for Semantic Search
client=chromadb.Client()
collection=client.create_collection("rag_docs")
collection.add(
    documents=chunks,
    ids=["id1","id2","id3","id4","id5"]
)
results=collection.query(
    query_texts=["semantic search embeddings"],
    n_results=2
)
# print(results)
# print(results['documents'])

#Step 5: Combine Both Result Sets
sematic_results=results['documents'][0]
combined_results=list(set(bm25_results[0]+sematic_results))
# print(combined_results)

# Step 7: Assign Semantic Scores
print('\n Step 7: Assign Semantic Scores')
semantic_scores={}
distance=results['distances'][0]
for docs,dist in zip(sematic_results,distance):
    semantic_scores[docs]=1 - dist
print(semantic_scores)

#Step 8: Combine Both Scores
print('\nStep 8: Combine Both Scores')
combined_scores = {}
for chunk in combined_results:
    combined_scores[chunk]=bm25_results[1].get(chunk,0)+semantic_scores.get(chunk,0)
print(combined_scores)

#Step 9: Final Ranked Top-K
print('\nStep 9: Final Ranked Top-K or hybrid Search Results')
ranked_results=sorted(combined_scores.items(), key=lambda x:x[1], reverse=True)
# print(ranked_results)
for doc,score in ranked_results:
    print(f'Score : {score:.4f} | {doc}')

#Step 10: Test Edge Cases
print('\nStep 10: Test Edge Cases')
bm25_results2,bm25_scores2=search_bm25('BM25 algorithm',bm25)
print("BM25 found : ",bm25_results2)
results2=collection.query(
    query_texts=['Vector similarity search'],
    n_results=2
)
print('Semantic_search found : ',results2['documents'][0])
