## Day 58 - Code Refactoring

- Refactoring means improving how code is organized without changing what it does —
  same inputs, same outputs, better structure for teammates and future me.

- Key habits I built today: avoid hardcoded magic numbers (use named constants),
  never overload one function with multiple jobs (Single Responsibility Principle),
  always catch specific exceptions like `redis.RedisError` not bare `except:`.

- Tools like `black` and `ruff` handle style automatically so code reviews focus
  on logic, not formatting — this speeds up team collaboration significantly.