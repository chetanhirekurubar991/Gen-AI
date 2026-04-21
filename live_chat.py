from langchain.agents import create_agent
from langchain_community.chat_models import ChatOllama
from langchain.tools import tool
from tavily import TavilyClient
import os

# ✅ API key
os.environ["TAVILY_API_KEY"] = "your_api_key"

tavily = TavilyClient()

# ✅ Web tool (IMPORTANT)
@tool
def search_web(query: str) -> str:
    """Search latest real-time information from internet"""
    results = tavily.search(query=query, max_results=3)
    return str(results)

# ✅ Local Qwen model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

tools = [search_web]

# ✅ Agent
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="Always use search_web tool for latest or real-time information."
)

# ✅ Run
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Yesterday IPL match result with full scorecard"}
        ]
    }
)

print(response)