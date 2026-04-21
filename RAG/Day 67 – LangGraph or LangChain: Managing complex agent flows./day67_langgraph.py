from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="qwen3:4b")
def execute_tool(message):
    return f"Tool result for: {message.content}"
class AgentState(TypedDict):
    messages:list
    status: str
    steps_taken: int

def llm_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages":messages + [response],
        "status":"running",
        "steps_taken":state["steps_taken"]+1
    }

def tool_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]
    tool_result = execute_tool(last_message)

    return {
        "messages": messages + [tool_result],
        "status":"running",
        "steps_taken": state["steps_taken"]+1
    }

def should_continue(state:AgentState) -> str:
    if state["status"] == "failed":
        return "end"
    if state["steps_taken"] >=3:
        return "end"
    if len(state["messages"]) > 10:
        return "end"
    return "continue"

graph = StateGraph(AgentState)

graph.add_node("llm",llm_node)
graph.add_node("tool",tool_node)

graph.set_entry_point("llm")

graph.add_conditional_edges("llm",should_continue,{
    "continue":"tool",
    "end":END
})
graph.add_edge("tool","llm")

app=graph.compile()

result = app.invoke(
    {
        "messages":[HumanMessage(content="Search Python and calculate 10+20")],
        "status":"running",
        "steps_taken":0
    },
    config={"recursion_limit":5}
)

print(result)