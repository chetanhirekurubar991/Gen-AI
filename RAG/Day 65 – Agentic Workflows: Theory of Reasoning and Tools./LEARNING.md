## Day 65 — Agentic Workflows

- An AI Agent is different from a chain because it loops 
  back and forth — each step depends on the previous result, 
  requires memory to track progress, and uses tools to 
  act on the world. A chain just executes fixed steps.

- The ReAct pattern works by cycling: Thought → Action → 
  Observation → Thought → Action → Observation... until 
  the task is complete. The agent reasons about what it 
  observed before deciding the next action.

- The #1 safety rule for agents is Human-in-the-Loop — 
  pause and get human approval before any irreversible 
  action (sending money, emails, deleting data) to avoid 
  unrecoverable loss.