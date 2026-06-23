#!/usr/bin/env python3
"""Subagents Demo：主 Agent 调度多个专家 Agent"""
#把不同能力封装成工具，让主 Agent 自动选择调用
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# =========================================================
# 1️⃣ 定义“专家工具”（本质就是子 Agent）
# =========================================================

@tool
def weather_agent(city: str) -> str:
    """天气专家：回答天气问题"""
    return f"{city} 今天晴天，25°C，非常适合出门。"


@tool
def math_agent(expression: str) -> str:
    """数学专家：计算简单表达式"""
    try:
        return f"计算结果是：{eval(expression)}"
    except Exception:
        return "表达式无法计算"


# =========================================================
# 2️⃣ 初始化 LLM（主控大脑）
# =========================================================

llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)


# =========================================================
# 3️⃣ 创建主 Agent（核心：把子 Agent 当工具）
# =========================================================

agent = create_agent(
    model=llm,
    tools=[weather_agent, math_agent],
    system_prompt="""
你是一个调度型Agent，你可以使用工具解决问题：

- weather_agent：处理天气问题
- math_agent：处理数学计算问题

遇到问题请选择合适工具。
""",
)


# =========================================================
# 4️⃣ 测试 Subagents 调度
# =========================================================

print("\n===== 测试1：天气问题 =====")
result1 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "北京今天天气怎么样？"
    }]
})
print(result1["messages"][-1].content)


print("\n===== 测试2：数学问题 =====")
result2 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "帮我算一下 123 * 456"
    }]
})
print(result2["messages"][-1].content)