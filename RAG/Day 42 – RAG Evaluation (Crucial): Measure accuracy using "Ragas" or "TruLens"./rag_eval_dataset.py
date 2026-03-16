# rag_eval_dataset.py
# Your mini evaluation dataset — 3 questions is enough to start

eval_dataset = [
    {
        "question": "What is RAG in AI?",
        "ground_truth": "RAG stands for Retrieval-Augmented Generation. It combines a retrieval system with a language model to answer questions using external documents.",
        "contexts": [
            "RAG stands for Retrieval-Augmented Generation. It is a technique that retrieves relevant documents from a knowledge base and passes them to an LLM to generate grounded answers."
        ],
        "answer": "RAG is Retrieval-Augmented Generation, a method that fetches relevant documents and uses them to generate accurate answers with an LLM."
    },
    {
        "question": "What is a vector database?",
        "ground_truth": "A vector database stores data as numerical vectors and enables fast similarity search, commonly used in RAG pipelines.",
        "contexts": [
            "A vector database stores embeddings — numerical representations of text. It allows similarity search so the most relevant documents can be retrieved quickly."
        ],
        "answer": "A vector database stores text as numerical vectors and retrieves the most similar ones during a search query."
    },
    {
        "question": "What is chunking in RAG?",
        "ground_truth": "Chunking is splitting large documents into smaller pieces so they can be embedded and retrieved more effectively.",
        "contexts": [
            "Chunking refers to breaking down large documents into smaller text segments before embedding them into a vector database, improving retrieval accuracy."
        ],
        "answer": "Chunking means splitting documents into smaller parts to make retrieval more precise in a RAG system."
    }
]

print(f"✅ Dataset loaded: {len(eval_dataset)} samples ready.")