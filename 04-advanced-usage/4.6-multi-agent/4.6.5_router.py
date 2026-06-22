#!/usr/bin/env python3
"""Router Demo：路由器模式（先分类再分发）"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# =========================================================
# 1️⃣ 定义不同领域的“专用 Agent（工具化）”
# =========================================================

@tool
def weather_agent(query: str) -> str:
    """天气Agent"""
    return f"天气结果：{query} → 今天晴天，适合出行。"


@tool
def code_agent(query: str) -> str:
    """代码Agent"""
    return f"代码结果：已为你生成 Python 示例代码：print('Hello World')"


@tool
def translate_agent(query: str) -> str:
    """翻译Agent"""
    return f"翻译结果：{query} → Hello World"


# =========================================================
# 2️⃣ 初始化 LLM（路由大脑）
# =========================================================

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-xxx",
    base_url="https://api.deepseek.com",
    temperature=0,
)


# =========================================================
# 3️⃣ 创建 Router Agent（核心）
# =========================================================

agent = create_agent(
    model=llm,
    tools=[weather_agent, code_agent, translate_agent],
    system_prompt="""
你是一个路由器Agent，你的任务是：

先判断用户问题类型，然后选择合适工具：

- 天气问题 → weather_agent
- 代码问题 → code_agent
- 翻译问题 → translate_agent

你只负责“分类+调用”，不要自己回答。
""",
)


# =========================================================
# 4️⃣ 测试 Router
# =========================================================

print("\n===== 测试1：天气问题 =====")
result1 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "北京今天天气怎么样？"
    }]
})
print(result1["messages"][-1].content)


print("\n===== 测试2：代码问题 =====")
result2 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "帮我写一个Python打印hello world"
    }]
})
print(result2["messages"][-1].content)


print("\n===== 测试3：翻译问题 =====")
result3 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "把 hello world 翻译成中文"
    }]
})
print(result3["messages"][-1].content)