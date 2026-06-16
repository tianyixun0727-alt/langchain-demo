#!/usr/bin/env python3
"""Agentic RAG — 从真实网站获取数据并回答（兼容 0.3.30）"""

import requests
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

# ========== Tools ==========

@tool
def fetch_modelscope_models(keyword: str) -> str:
    """从 ModelScope 获取 AI 模型信息"""
    try:
        resp = requests.get(
            f"https://modelscope.cn/api/v1/models?PageSize=5&Search={keyword}",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        data = resp.json()
        models = data.get("Data", {}).get("Models", [])

        if not models:
            return f"未找到关于 '{keyword}' 的模型"

        result = []
        for m in models:
            name = m.get("ModelName", m.get("Name", "未知"))
            task = m.get("TaskName", "通用")
            result.append(f"模型名称: {name} | 任务类型: {task}")

        return "\n".join(result)

    except Exception as e:
        return f"获取数据失败: {e}"


@tool
def search_github_repos(query: str) -> str:
    """从 GitHub 搜索开源项目"""
    try:
        resp = requests.get(
            f"https://api.github.com/search/repositories?q={query}&sort=stars&per_page=5",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        repos = resp.json().get("items", [])

        if not repos:
            return f"未找到关于 '{query}' 的项目"

        result = []
        for r in repos:
            result.append(
                f"""
项目: {r['full_name']}
描述: {r.get('description','无')}
星标: {r['stargazers_count']}
语言: {r.get('language','未知')}
链接: {r['html_url']}
"""
            )
        return "\n---\n".join(result)

    except Exception as e:
        return f"获取数据失败: {e}"


# ========== Agent ==========
tools = [fetch_modelscope_models, search_github_repos]

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# ========== Demo ==========
print("=" * 60)
print("Agentic RAG 演示 — 实时检索 + 生成")
print("=" * 60)
print()

print(">>> 问题1: ModelScope 对话模型")
result1 = executor.invoke({
    "input": "ModelScope 上有哪些对话模型？列出名称和任务类型"
})
print(result1["output"][:300])
print()

print(">>> 问题2: GitHub LangChain 热门项目")
result2 = executor.invoke({
    "input": "GitHub 上关于 LangChain 的热门项目有哪些？"
})
print(result2["output"][:300])
print()

print("=" * 60)
print("RAG 工作原理")
print("=" * 60)
print("""
Agentic RAG 流程:
1. 收到用户问题
2. Agent 判断是否需要调用工具
3. 调用 ModelScope / GitHub API
4. 获取外部知识
5. LLM 综合生成答案

三种 RAG 架构:
• 2-Step RAG
• Agentic RAG
• Hybrid RAG
""")