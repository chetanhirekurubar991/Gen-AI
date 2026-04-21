## Day 68 — System Design: ChatGPT

- System design is about trade-offs, not just components. 
  Reducing latency raises cost, adding safety raises latency — 
  every decision negotiates between the four constraints: 
  latency, scale, cost, safety.

- LLMs cannot be served like REST APIs. Each token requires 
  a full GPU pass — you need queues, batching, and streaming 
  to serve 10K concurrent users without burning cost.

- Memory has three layers: Redis (active session), 
  Vector DB (semantic recall via RAG), SQL (permanent history). 
  Context overflow is solved by sliding window + summarisation + RAG together.