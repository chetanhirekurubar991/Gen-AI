# step2_retrieve.py
# PURPOSE: Load existing Chroma store and retrieve relevant chunks with metadata

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def load_vectorstore(persist_directory: str = "vectorstore"):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = Chroma(
        persist_directory=persist_directory, embedding_function=embedding_model
    )
    return vectorstore


def retrieve_chunks_with_metadata(vectorstore, query: str, k: int = 3):
    results = vectorstore.similarity_search(query, k=k)
    retrieved = []
    for chunk in results:
        retrieved.append(
            {
                "content": chunk.page_content,
                "page_number": chunk.metadata.get("page_number", "unknown"),
                "source": chunk.metadata.get("source", "unknown"),
                "category": chunk.metadata.get("category", "unknown"),
            }
        )
    return retrieved


if __name__ == "__main__":
    store = load_vectorstore()
    results = retrieve_chunks_with_metadata(
        store, query="What is CRYSTAL CODER trained on?", k=3
    )
    for i, r in enumerate(results):
        print(f"\n --Chunks {i+1}")
        print(f"Page : {r['page_number']}")
        print(f"Source : {r['source']}")
        print(f"Content : {r['content'][:150]}")
