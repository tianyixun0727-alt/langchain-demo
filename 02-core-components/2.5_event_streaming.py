#!/usr/bin/env python3
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

@tool
def get_weather(city: str) -> str:
    """获取天气"""
    return f"{city} 天气晴朗"

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com",
    temperature=0
)

# 使用 create_react_agent 替代 create_agent
agent = create_react_agent(model=llm, tools=[get_weather])

# 流式输出（打字机效果）
for chunk in agent.stream(
    {"messages": [("user", "北京天气如何？")]},
    stream_mode="messages"
):
    # 每个 chunk 是 (message, metadata) 元组
    if isinstance(chunk, tuple) and len(chunk) == 2:
        msg, _ = chunk
        if hasattr(msg, "content") and msg.content:
            print(msg.content, end="", flush=True)
print()