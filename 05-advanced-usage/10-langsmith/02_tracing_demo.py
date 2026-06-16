#!/usr/bin/env python3
"""LangSmith Tracing Demo — Setting up observability"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

@tool
def get_timezone(city: str) -> str:
    """获取城市时区信息"""
    return f"{city} is in UTC+8"

agent = create_agent(
    llm=llm,
    tools=[get_timezone],
    system_prompt="You are a helpful assistant.",
)

print("""
=== LangSmith Tracing Demo ===

To enable tracing, set these environment variables BEFORE running:

  export LANGSMITH_TRACING=true
  export LANGSMITH_API_KEY="lsv2_..."

Then run this script — all agent calls will be automatically traced
and viewable at https://smith.langchain.com

Tracing captures:
  • Each model call (with prompt and response)
  • Each tool execution (with input and output)
  • State transitions between steps
  • Full execution timeline with latency
  • Token usage and cost estimates

Tip: You can also trace specific components by adding
     tags and metadata to your agent configuration.
""")

# Without tracing enabled, show a basic invocation
print("\\n=== Agent Invocation (trace when LANGSMITH_TRACING=true) ===\\n")
result = agent.invoke({
    "messages": [{"role": "user", "content": "What timezone is Tokyo in?"}]
})
print(f"Result: {result['messages'][-1]['content']}")
