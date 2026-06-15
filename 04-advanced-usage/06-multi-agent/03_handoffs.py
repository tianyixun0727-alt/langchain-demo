#!/usr/bin/env python3
"""交接模式 — 根据问题类型自动转接"""

import requests
from langchain.agents import create_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

# 状态变量：记录当前由哪个智能体处理
current_agent = {"name": "前台接待"}

@tool
def search_modelscope(keyword: str) -> str:
    """在 ModelScope 搜索 AI 模型"""
    try:
        resp = requests.get(
            f"https://modelscope.cn/api/v1/models?PageSize=3&Search={keyword}",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        models = resp.json().get("Data", {}).get("Models", [])
        return "\n".join(f"• {m.get('ModelName','?')}" for m in models[:3]) or "未找到"
    except Exception as e:
        return f"错误: {e}"

@tool
def transfer_to_tech_support(issue: str) -> str:
    """转接给技术支持，处理技术问题"""
    current_agent["name"] = "技术支持"
    return f"已转接给技术支持。问题: {issue}"

@tool
def transfer_to_model_expert(query: str) -> str:
    """转接给模型专家，处理模型推荐问题"""
    current_agent["name"] = "模型专家"
    return f"已转接给模型专家。查询: {query}"

# 前台接待智能体
front_desk = create_agent(
    llm=llm,
    tools=[transfer_to_tech_support, transfer_to_model_expert],
    system_prompt="""你是前台接待。判断用户问题:
- 技术问题 → transfer_to_tech_support
- 模型推荐 → transfer_to_model_expert
- 其他 → 直接回复"""
)

# 模型专家智能体（演示用）
model_expert = create_agent(
    llm=llm,
    tools=[search_modelscope],
    system_prompt="你是模型专家。使用 search_modelscope 搜索模型。"
)

print("=" * 60)
print("交接模式 — 智能问题转接")
print("=" * 60)

questions = [
    "帮我推荐一个对话模型",
    "我的代码报错了, 怎么修复?",
]

for q in questions:
    print(f"\n>>> 用户提问: {q}")
    result = front_desk.invoke({
        "messages": [{"role": "user", "content": q}]
    })
    print(f"   → 转接至: {current_agent['name']}")
    print(f"   → 响应: {result['messages'][-1]['content'][:150]}")
    current_agent["name"] = "前台接待"  # 重置

print("\n" + "=" * 60)
print("交接模式说明")
print("=" * 60)
print("""
工作流程:
  1. 前台接待接收用户问题
  2. 判断问题类型，调用 transfer_to_* 工具
  3. 状态更新，切换到对应智能体
  4. 专业智能体处理问题

这种模式适用于:
  • 客服中心 — 根据问题类型自动升级
  • 技术支持 — 一线接待 → 二线专家
  • 多领域问答 — 识别领域后转交
""")
