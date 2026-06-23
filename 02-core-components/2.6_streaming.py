#!/usr/bin/env python3
"""流式输出"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

print("=== Token Streaming ===")
for chunk in llm.stream([
    {"role": "user", "content": "Count from 1 to 5."}
]):
    print(chunk.content, end="", flush=True)
print("\n")

print("=== Agent Streaming ===")


agent = create_agent(model=llm, tools=[])

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Say hello!"}]
}):
    if "messages" in chunk:
        print(chunk["messages"][-1])
#模型流式输出，是模型边生成边输出。
#智能体流式输出，是整个智能体执行过程边执行边输出。