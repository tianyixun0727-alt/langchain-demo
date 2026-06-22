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
#把普通 Python 函数变成 LLM 可调用的工具,模拟了一个天气 API：输入城市名称 返回天气结果


llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)#这一部分我们初始化了语言模型 ChatOpenAI。
#虽然名字是 OpenAI，但其实支持任何兼容 OpenAI API 的模型，比如 DeepSeek。

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
print(result["messages"][-1]["content"])
