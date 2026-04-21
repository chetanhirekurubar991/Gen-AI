# Day 43 — Citations in RAG

## What I Built
A citation-verified RAG pipeline that retrieves chunks from 
Chroma, forces the LLM to cite page numbers from metadata, 
and validates that every cited page was actually retrieved 
— not invented by the LLM.

## 3 Key Learnings
- Citations must come from Vector DB metadata, not LLM memory.
  The LLM only repeats back what we explicitly put in the prompt.
  
- SemanticChunker splits by meaning shift, not character count.
  This preserves sentence context and improves retrieval accuracy.
  
- Embedding model and generation model should be separate.
  BAAI/bge is purpose-built for retrieval. LLMs are for reasoning.

## Mistakes I Almost Made
- Using page + 1 instead of page_label. Would have shown wrong 
  page numbers for PDFs with Roman numeral intro pages.
  
- Using same model for embedding and generation. Would have 
  reduced retrieval accuracy and wasted compute.

## One Thing I'd Do Differently
Add server-side validation — verify the cited content actually 
exists in the chunk text, not just that the page number matches.
