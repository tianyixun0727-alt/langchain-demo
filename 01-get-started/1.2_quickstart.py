#!/usr/bin/env python3
"""第一个 LangChain 智能体 - 天气查询"""

#导入三个核心组件
from langchain.agents import create_agent #创建智能体
from langchain.tools import tool #定义工具
from langchain_openai import ChatOpenAI #调用大模型


@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"It's always sunny in {city}!"


llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

agent = create_agent(
    model=llm,
    tools=[get_weather],#提供外部能力（天气查询）
    system_prompt="You are a helpful assistant",#控制行为风格
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What's the weather in San Francisco?"
    }]
})
print(result["messages"][-1].content)
