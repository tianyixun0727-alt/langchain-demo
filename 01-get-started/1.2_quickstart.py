#!/usr/bin/env python3
"""第一个 LangChain 智能体 - 天气查询"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"It's always sunny in {city}!"

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

agent = create_agent(
    llm=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What's the weather in San Francisco?"
    }]
})
print(result["messages"][-1]["content"])
