## Day 69: System Design — Scaling Vector DBs

- **Scaling Strategy:** Local ChromaDB breaks at 1M+ vectors
  (30GB+ RAM). Solution: Shard by document type/user,
  add Query Router + Merger + Read Replicas.

- **Index Trade-offs:** HNSW (fast, 90-99% recall) for
  production RAG. IVF-PQ (memory efficient) for 100M+
  vectors. Flat index for medical/legal (100% accuracy required).

- **Cost Optimization:** Semantic Redis caching reduces
  query costs ~40%. Self-hosted Qdrant breaks even with
  Pinecone at ~12.5M queries/month (~$500/month flat
  vs $1,267/month managed).