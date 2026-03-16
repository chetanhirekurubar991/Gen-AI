## Day 56 — Caching with Redis

- **What is caching:** Instead of calling the LLM every time for the 
  same question, I store the first response in Redis. Same question = 
  instant answer from cache, zero LLM cost.

- **Why it matters for cost and speed:** LLM responses take 1-5 seconds 
  and cost tokens on every call. Redis answers in ~1ms from RAM. 
  In production with thousands of users, this saves significant money 
  and improves user experience dramatically.

- **What I learned the hard way:** A missing `networks:` in one Docker 
  service silently breaks container communication. Always verify every 
  service is on the same network, and use startup logs to catch 
  connection errors early (Day 52 logging saved me here).