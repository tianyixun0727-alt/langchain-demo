#!/usr/bin/env python3
"""Single Agent Pattern — The simplest pattern for most use cases"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

@tool
def add(a: float, b: float) -> float:
    """将两个数字相加"""
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """将两个数字相乘"""
    return a * b

agent = create_agent(
    llm=llm,
    tools=[add, multiply],
    system_prompt="You are a math assistant. Use the available tools.",
)

print("=== Single Agent Pattern Demo ===")
result = agent.invoke({
    "messages": [{"role": "user", "content": "Calculate (3 + 5) * 2"}]
})
print(f"Result: {result['messages'][-1]['content']}")
