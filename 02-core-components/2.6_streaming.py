#!/usr/bin/env python3
"""流式输出"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

# ========== 1. 模型流式输出：逐 token 输出 ==========
print("=== Token Streaming ===")
for chunk in llm.stream([
    {"role": "user", "content": "Count from 1 to 5."}
]):
    print(chunk.content, end="", flush=True)
print("\n")

# ========== 2. 智能体流式输出：按节点逐步输出 ==========
print("=== Agent Streaming (values) ===")

from langchain.tools import tool   # 仅在此处导入，不影响其他部分

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city}：晴，气温 25°C"

agent = create_agent(model=llm, tools=[get_weather])   # 传入工具

for event in agent.stream(
    {"messages": [{"role": "user", "content": "北京天气如何？"}]},   # 需要工具的问题
    stream_mode="values",
):
    if "messages" in event:
        msg = event["messages"][-1]
        role = type(msg).__name__
        print(f"[{role}] {msg.content}")

print()

# 模型流式输出，是模型边生成边输出。
# 智能体流式输出，是整个智能体执行过程边执行边输出。