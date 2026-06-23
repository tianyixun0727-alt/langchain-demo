#!/usr/bin/env python3
"""LangChain 智能体 - 流式天气查询"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city} 天气晴朗"


llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# ✅ 正确的流式事件接口
events = agent.stream(
    {"messages": [{"role": "user", "content": "北京天气如何？"}]}
)

# ✅ 逐事件处理（真正 streaming）
for event in events:
    # 每个 event 结构可能不同，这里做兼容处理
    if "messages" in event:
        msg = event["messages"][-1]

        if hasattr(msg, "content"):
            print(msg.content, end="", flush=True)

        elif isinstance(msg, dict) and "content" in msg:
            print(msg["content"], end="", flush=True)

print()