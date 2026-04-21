## Day 70 – GenAI Security: Prompt Injection attacks & defense.
- Learned that agent tools are the highest-risk attack surface 
  because a compromised agent can execute real-world actions 
  (delete data, send emails). Defense: human-in-the-loop approval 
  gates before any destructive tool executes.
- Learned that single-point filtering fails against GenAI attacks. 
  Implemented three-gate defense: input scanning before LLM, 
  behavior monitoring during execution, output filtering before 
  response reaches user.
- Learned three critical failure modes in unsecured GenAI systems: 
  infinite loop attacks exhaust compute resources, tool hijacking 
  enables mass data deletion, and dangerous tool combinations 
  (read + email) enable silent data exfiltration.