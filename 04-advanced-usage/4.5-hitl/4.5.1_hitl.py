#!/usr/bin/env python3
"""Human-in-the-Loop Demo: 邮件发送审批"""

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
import json

# ---------- 1. 定义工具 ----------
@tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """发送邮件"""
    return f"✅ 邮件已发送至 {recipient}"

@tool
def get_weather(city: str) -> str:
    """获取天气（无需审批）"""
    return f"{city} 天气晴朗"

# ---------- 2. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

# ---------- 3. 创建 HITL 中间件 ----------
hitl = HumanInTheLoopMiddleware(
    interrupt_on={
        "send_email": {
            "allowed_decisions": ["approve", "edit", "reject"],
            "description": "⚠️ 即将发送邮件，请审批"
        }
    }
)

# ---------- 4. 创建 Agent ----------
agent = create_agent(
    model=llm,
    tools=[send_email, get_weather],
    middleware=[hitl],
    checkpointer=InMemorySaver(),  # 必须配置，用于保存中断状态
)

config = {"configurable": {"thread_id": "demo-001"}}

# ---------- 5. 触发中断 ----------
print("=== 用户请求发送邮件 ===")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "给 alice@example.com 发邮件，主题：你好，内容：测试"}]},
    config=config
)

# ---------- 6. 检查是否中断 ----------
if "__interrupt__" in result:
    print("\n⏸️ Agent 已暂停，等待审批...")
    interrupt = result["__interrupt__"][0].value
    print(f"待审批工具: {interrupt}")

    # ---------- 7. 模拟人工决策 ----------
    # 场景1：批准（✅ 当前启用）
    decision = {"decisions": [{"type": "approve"}]}

    # 场景2：编辑（修改内容）
    # decision = {
    #     "decisions": [{
    #         "type": "edit",
    #         "edited_action": {
    #             "name": "send_email",
    #             "args": {"recipient": "alice@example.com", "subject": "你好", "body": "【修改】这是测试邮件"}
    #         }
    #     }]
    # }

    # 场景3：拒绝（已注释）
    # decision = {
    #     "decisions": [{
    #         "type": "reject",
    #         "reason": "邮件内容需要补充更多信息"
    #     }]
    # }

    print(f"\n👤 人工决策: {decision}")
    result = agent.invoke(Command(resume=decision), config=config)

# ---------- 8. 输出结果 ----------
print("\n=== 最终结果 ===")
print(result["messages"][-1].content)