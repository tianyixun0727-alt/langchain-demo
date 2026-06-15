#!/usr/bin/env python3
"""流式输出"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

print("=== Token Streaming ===")
for chunk in llm.stream([
    {"role": "user", "content": "Count from 1 to 5."}
]):
    print(chunk.content, end="", flush=True)
print("\n")

print("=== Agent Streaming ===")


agent = create_agent(llm=llm, tools=[])
for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Say hello!"}]
}):
    if "messages" in chunk:
        print(chunk["messages"][-1])
