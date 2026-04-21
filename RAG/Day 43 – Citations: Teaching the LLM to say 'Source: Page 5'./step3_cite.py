import requests
import re
from step2_retrive import load_vectorstore, retrieve_chunks_with_metadata


def build_citation_prompt(query: str, retrieved_chunks: list) -> str:
    context_blocks = []
    for chunk in retrieved_chunks:
        block = f"[Source:Page {chunk['page_number']}]\n{chunk['content']}"
        context_blocks.append(block)
    full_context = "\n\n".join(context_blocks)
    prompt = f"""You are a precise research assistant.
Answer the question using ONLY the context provided below.
Every claim you make MUST cite its source like this: [Source: Page X]
Do not use any outside knowledge. If the answer is not in the context, say "Not found in document."

CONTEXT: {full_context}

QUESTION:{query}
ANSWER:"""
    return prompt


def ask_llm_with_citations(prompt: str, model: str = "qwen3:4b") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )
    result = response.json()
    return result["response"]


def validate_citation(answer: str, retrieved_chunks: list) -> dict:
    cited_pages = re.findall(r"\[Source: Page (\w+)\]", answer)
    retrieved_pages = [chunk["page_number"] for chunk in retrieved_chunks]
    validation_results = {}
    for page in cited_pages:
        validation_results[page] = page in retrieved_pages
    return {
        "cited_pages": cited_pages,
        "retrieved_pages": retrieved_pages,
        "validation": validation_results,
        "all_valid": all(validation_results.values()),
    }


if __name__ == "__main__":
    store = load_vectorstore()
    query = "What is CRYSTAL CODER trained on?"
    chunks = retrieve_chunks_with_metadata(store, query=query, k=4)

    prompt = build_citation_prompt(query=query, retrieved_chunks=chunks)

    answer = ask_llm_with_citations(prompt)
    print("=" * 15, " LLM ANSWER ", "=" * 15)
    print(answer)
    print("=" * 40)

    validation = validate_citation(answer, chunks)
    print("=" * 15, " CITATION VALIDATION ", "=" * 15)
    print(f"LLM cited pages : {validation['cited_pages']}")
    print(f'Retrieved pages : {validation["retrieved_pages"]}')
    print(f"Validation results : {validation['validation']}")
    print(f"All citation valid : {validation['all_valid']}")
    print("=" * 40)
