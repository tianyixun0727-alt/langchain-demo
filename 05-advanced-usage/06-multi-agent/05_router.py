#!/usr/bin/env python3
"""路由器模式 — 根据问题类型分发到不同智能体"""

import requests
from langchain.agents import create_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

# 工具：调用外部 API
def fetch_github_trending(language="python"):
    """获取 GitHub 热门仓库"""
    try:
        resp = requests.get(
            f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&per_page=3",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        repos = resp.json().get("items", [])
        return "\n".join(f"• {r['full_name']} ⭐{r['stargazers_count']}" for r in repos[:3])
    except Exception as e:
        return f"获取失败: {e}"

# 各领域专用智能体
python_agent = create_agent(
    llm=llm,
    tools=[],
    system_prompt="你是 Python 技术专家。回答 Python 相关问题。"
)

ai_agent = create_agent(
    llm=llm,
    tools=[],
    system_prompt="你是 AI 领域专家。回答 AI、机器学习、深度学习相关问题。"
)

general_agent = create_agent(
    llm=llm,
    tools=[],
    system_prompt="你是通用助手，回答各类问题。"
)

# 路由器函数
def route_query(query: str):
    """根据问题内容分发到对应智能体"""
    q = query.lower()
    if any(kw in q for kw in ["python", "django", "flask", "pytorch"]):
        return python_agent, "Python 专家"
    elif any(kw in q for kw in ["ai", "模型", "大模型", "gpt", "llm", "深度学习"]):
        return ai_agent, "AI 专家"
    else:
        return general_agent, "通用助手"

print("=" * 60)
print("路由器模式 — 智能分发演示")
print("=" * 60)

test_queries = [
    "如何在 Python 中处理 JSON 数据?",
    "什么是大语言模型?",
    "今天天气怎么样?",
]

for q in test_queries:
    agent, name = route_query(q)
    print(f"\n>>> 问题: {q}")
    print(f"   → 路由至: {name}")
    result = agent.invoke({"messages": [{"role": "user", "content": q}]})
    print(f"   → 回答: {result['messages'][-1]['content'][:150]}")

print("\n📊 热门 GitHub Python 项目:")
print(fetch_github_trending("python"))

print("\n" + "=" * 60)
print("路由器模式说明")
print("=" * 60)
print("""
架构:
              ┌─ Python 专家
  用户 → 路由器 ── AI 专家
              └─ 通用助手

适用场景:
  • 智能客服 — 按业务领域分发
  • 多模态输入 — 按内容类型路由
  • 微服务集成 — 按服务类型调度
""")
