#!/usr/bin/env python3
"""LangChain 智能体 - invoke 与 stream 对比"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
    base_url="http://10.187.126.181:3000/v1",
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


# ========== 方式1: invoke —— 一次性返回完整结果 ==========
print("=" * 50)
print("方式1: agent.invoke() - 一次性返回完整结果")
print("=" * 50)
result = agent.invoke({"messages": [{"role": "user", "content": "北京天气如何？"}]})
print(result["messages"][-1].content)
print()


# ========== 方式2: stream（messages 模式）—— 逐 token 流式输出 ==========
print("=" * 50)
print("方式2: agent.stream(stream_mode='messages') - 逐 token 流式")
print("=" * 50)
events = agent.stream(
    {"messages": [{"role": "user", "content": "上海天气如何？"}]},
    stream_mode="messages",
)
for chunk, metadata in events:
    if type(chunk).__name__ == "AIMessageChunk" and chunk.content:
        print(chunk.content, end="", flush=True)
print("\n")


# ========== 核心区别 ==========
print("=" * 50)
print("invoke  : 等待全部生成后一次性返回，适合批量处理")
print("stream  : 边生成边返回，适合实时交互（打字机效果）")
print("=" * 50)