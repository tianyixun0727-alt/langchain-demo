#!/usr/bin/env python3
"""Skills Demo：按需加载能力（技能系统）"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# =========================================================
# 1️⃣ 定义“技能模块”（Skills）
# =========================================================

@tool
def sql_skill(query: str) -> str:
    """SQL技能：生成SQL查询语句"""
    return f"SELECT * FROM users WHERE condition = '{query}';"


@tool
def python_skill(code: str) -> str:
    """Python技能：解释或执行代码"""
    try:
        return str(eval(code))
    except Exception:
        return "无法执行该Python表达式"


@tool
def translate_skill(text: str) -> str:
    """翻译技能：模拟中英翻译"""
    return f"翻译结果：{text} (translated)"


# =========================================================
# 2️⃣ 初始化 LLM
# =========================================================

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-xxx",
    base_url="https://api.deepseek.com",
    temperature=0,
)


# =========================================================
# 3️⃣ 创建 Agent（技能系统）
# =========================================================

agent = create_agent(
    model=llm,
    tools=[sql_skill, python_skill, translate_skill],
    system_prompt="""
你是一个“技能型Agent”。

你拥有以下能力：
- sql_skill：生成SQL
- python_skill：执行Python逻辑
- translate_skill：翻译文本

你必须根据用户问题，按需调用对应技能，而不是自己直接回答。
""",
)


# =========================================================
# 4️⃣ 测试 Skills
# =========================================================

print("\n===== 测试1：SQL任务 =====")
result1 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "帮我查一下用户表里名字叫Tom的数据"
    }]
})
print(result1["messages"][-1].content)


print("\n===== 测试2：Python任务 =====")
result2 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "计算 2 + 3 * 10"
    }]
})
print(result2["messages"][-1].content)


print("\n===== 测试3：翻译任务 =====")
result3 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "把 hello world 翻译一下"
    }]
})
print(result3["messages"][-1].content)