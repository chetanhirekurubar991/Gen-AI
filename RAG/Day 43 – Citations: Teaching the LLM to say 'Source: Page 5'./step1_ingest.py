from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings


def load_documents(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs


def attach_custom_metadata(docs, category: str = "Research Paper"):
    for doc in docs:
        doc.metadata["page_number"] = doc.metadata["page_label"]
        doc.metadata["category"] = category
        doc.metadata["version"] = "v1"
    return docs


def chunk_and_store(docs, persist_directory: str = "vectorstore"):

    # Embedding model — purpose built for retrieval, NOT generation
    embeddings_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},  # mac: use "mps" for Apple Silicon speed
        # encode_kwargs={"normalize_embeddings":True}  # improves cosine similarity accuracy not needed mini (needed eg : BAAI/bge-base-en-v1.5)
    )

    # Split by meaning using the embedding model
    splitter = SemanticChunker(
        embeddings=embeddings_model, breakpoint_threshold_type="percentile"
    )
    chunks = splitter.split_documents(docs)

    # Store in Chroma — metadata travels with every chunk
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=persist_directory,
    )
    print(f"Total chunks stored: {len(chunks)}")
    print(f"Sample chunk metadata: {chunks[0].metadata}")
    return vectorstore


if __name__ == "__main__":
    docs = load_documents("documents/trans_opensource_llm.pdf")
    docs = attach_custom_metadata(docs)
    store = chunk_and_store(docs)
    print("Ingestion complete")
    # print(f"{docs}")
    # print(f"Total pages loaded: {len(docs)}")
    # print(f"\n First page metadata: {docs[0].metadata}")
    # print(f"\n First 100 Characters: {docs[0].page_content}")
    # print(f"\n First second metadata: {docs[1].metadata}")
    # print(f"\n Second 100 Characters: {docs[1].page_content}")
