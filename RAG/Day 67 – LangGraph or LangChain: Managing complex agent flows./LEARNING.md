## Day 67 - LangGraph ✅

- Built a stateful graph with TypedDict State, 
  llm_node, tool_node, and conditional edges.

- Fixed GraphRecursionError by using steps_taken 
  counter in should_continue instead of relying 
  only on message length.

- LangGraph gives explicit control over agent flow —
  I decide when to stop, not LangChain.

