"""
RAG Evaluation — Ragas 0.4.3 + Ollama (ACTUALLY WORKING)
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from openai import OpenAI
from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory
from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy

# ─────────────────────────────────────────────────────────
# 1. LLM
# ─────────────────────────────────────────────────────────
client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1",
)

llm = llm_factory(
    "deepseek-coder:6.7b",       # ← your model
    provider="openai",
    client=client,
    max_tokens=4096,
)

# ─────────────────────────────────────────────────────────
# 2. EMBEDDINGS
# ─────────────────────────────────────────────────────────
embeddings = embedding_factory(
    "huggingface",
    model="sentence-transformers/all-MiniLM-L6-v2",
)

# ─────────────────────────────���───────────────────────────
# 3. Dataset
# ─────────────────────────────────────────────────────────
samples = [
    SingleTurnSample(
        user_input="What is RAG in AI?",
        retrieved_contexts=[
            "RAG stands for Retrieval-Augmented Generation. It retrieves relevant "
            "documents and passes them to an LLM to generate grounded answers."
        ],
        response="RAG is Retrieval-Augmented Generation, a method that fetches relevant "
                 "documents and uses them to generate accurate answers with an LLM.",
        reference="RAG stands for Retrieval-Augmented Generation.",
    ),
    SingleTurnSample(
        user_input="What is a vector database?",
        retrieved_contexts=[
            "A vector database stores embeddings, which are numerical representations "
            "of text. It allows similarity search so the most relevant documents can be "
            "retrieved quickly."
        ],
        response="A vector database stores text as numerical vectors and retrieves "
                 "the most similar ones during a search query.",
        reference="A vector database stores data as numerical vectors and enables "
                  "fast similarity search.",
    ),
    SingleTurnSample(
        user_input="What is chunking in RAG?",
        retrieved_contexts=[
            "Chunking refers to breaking down large documents into smaller text "
            "segments before embedding them into a vector database, improving "
            "retrieval accuracy."
        ],
        response="Chunking means splitting documents into smaller parts to make "
                 "retrieval more precise in a RAG system.",
        reference="Chunking is splitting large documents into smaller pieces so "
                  "they can be embedded and retrieved more effectively.",
    ),
]

dataset = EvaluationDataset(samples=samples)

# ─────────────────────────────────────────────────────────
# 4. Evaluate
# ─────────────────────────────────────────────────────────
print("\n🔍 Running evaluation...\n")

result = evaluate(
    dataset=dataset,
    metrics=[Faithfulness(), AnswerRelevancy()],
    llms=llm,
    embeddings=embeddings,
)

print("\n✅ EVALUATION RESULTS:")
print(f"  🔹 Faithfulness     : {result['faithfulness']:.4f}")
print(f"  🔹 Answer Relevancy : {result['answer_relevancy']:.4f}")

df = result.to_pandas()
print("\n📊 Per-sample scores:")
print(df.to_string(index=False))