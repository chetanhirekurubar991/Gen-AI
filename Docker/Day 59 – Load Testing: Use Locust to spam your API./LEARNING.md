# Day 59 — Load Testing Learnings

- Load testing uses a separate locustfile.py to simulate real user 
  traffic against your API — without touching production code. 
  Locust spawns virtual users that hit your endpoints repeatedly, 
  revealing how your app behaves under pressure.

- A cache (Day 56 Redis pattern) is a performance shield under load. 
  When all 5 messages were cached, 200 users got 4ms responses with 
  zero failures. When 30% of requests bypassed cache (unique messages), 
  response times jumped to 10,000-35,000ms — proving cache is not 
  optional for GenAI apps.

- The real bottleneck in a GenAI app is NOT FastAPI or Python — it's 
  the LLM connection pool (rate limits). Our semaphore(10) showed that 
  50 users × 30% cache miss = queue buildup → silent failures 
  (users waiting 35 seconds leave, even if error rate shows 0%).