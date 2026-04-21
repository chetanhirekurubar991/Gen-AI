from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools import tool

@tool
def calculator(expression:str)->str:
    """Useful for math calculations. Input should be a math expression like '234 * 456'."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(char in allowed for char in expression):
            return "Error: Invalid characters in expression"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# print(calculator("234*456"))
# print(calculator("10/0"))
# print(calculator("__import__('os"))

@tool
def search(query:str)->str:
    """Useful for searching information about weather, python, and langchain."""
    mock_results = {
        "weather": "The weather today is sunny with 25°C.",
        "python": "Python is a high-level programming language.",
        "langchain": "LangChain is a framework for building LLM applications.",
    }

    for key in mock_results:
        if key in query.lower():
            return mock_results[key]
    return "No results found for: "+query

# print(search("what is the weather today?"))
# print(search("tell me about python"))
# print(search("who is the musk?"))

llm = ChatOllama(model="qwen3:4b")
tools = [calculator,search]
agent = create_agent(llm,tools)

response = agent.invoke({
    "messages":[("user","Who is Elon Musk?")]},
    config={"recursion_limit":5}
)
print(response["messages"][-1].content)
print(" "*5)
print(response)
