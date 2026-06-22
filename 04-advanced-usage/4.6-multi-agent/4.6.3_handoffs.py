#!/usr/bin/env python3
"""Handoffs Demo：Agent 任务转交（接力模式）"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# =========================================================
# 1️⃣ 定义两个“角色 Agent”（模拟客服系统）
# =========================================================

@tool
def support_agent(message: str) -> str:
    """客服Agent：处理普通咨询"""
    return f"[客服回复] 我已收到您的问题：{message}，请稍等处理。"


@tool
def refund_agent(order_id: str) -> str:
    """售后Agent：处理退款"""
    return f"[售后回复] 订单 {order_id} 已进入退款流程，将在3-5天到账。"


# =========================================================
# 2️⃣ LLM 初始化
# =========================================================

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-xxx",
    base_url="https://api.deepseek.com",
    temperature=0,
)


# =========================================================
# 3️⃣ 主 Agent（负责“转交”）
# =========================================================

agent = create_agent(
    model=llm,
    tools=[support_agent, refund_agent],
    system_prompt="""
你是一个客服系统的路由Agent：

规则：
- 普通问题 → support_agent
- 涉及退款 / 订单 → refund_agent

你的任务是判断并转交，不要自己回答。
""",
)


# =========================================================
# 4️⃣ 测试 Handoffs
# =========================================================

print("\n===== 测试1：普通问题 =====")
result1 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "我想问一下你们的服务时间"
    }]
})
print(result1["messages"][-1].content)


print("\n===== 测试2：退款问题 =====")
result2 = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "我要退款，订单号12345"
    }]
})
print(result2["messages"][-1].content)