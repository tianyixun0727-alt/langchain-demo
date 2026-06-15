#!/usr/bin/env python3
"""子智能体模式 — 多模型搜索协作"""

import requests
from langchain.agents import create_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

# 真实搜索工具
@tool
def search_modelscope(keyword: str) -> str:
    """在 ModelScope 上搜索 AI 模型"""
    try:
        resp = requests.get(
            f"https://modelscope.cn/api/v1/models?PageSize=3&Sort=GmtCreate&Search={keyword}",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        data = resp.json()
        models = data.get("Data", {}).get("Models", [])
        if not models:
            return "未找到相关模型"
        results = []
        for m in models[:3]:
            results.append(f"• {m.get('ModelName','?')} - {m.get('TaskName','通用')}")
        return "\n".join(results)
    except Exception as e:
        return f"搜索失败: {e}"

@tool
def search_huggingface(keyword: str) -> str:
    """在 HuggingFace 上搜索热门模型"""
    try:
        resp = requests.get(
            f"https://huggingface.co/api/models?search={keyword}&sort=downloads&limit=3",
            timeout=10
        )
        models = resp.json()
        results = []
        for m in models[:3]:
            results.append(f"• {m.get('modelId','?')} (下载: {m.get('downloads',0):,})")
        return "\n".join(results) if results else "未找到模型"
    except Exception as e:
        return f"搜索失败: {e}"

# 子智能体 1: 模型搜索专家
model_search_agent = create_agent(
    llm=llm,
    tools=[search_modelscope, search_huggingface],
    system_prompt="你是 AI 模型搜索专家。当用户询问模型时，同时在 ModelScope 和 HuggingFace 上搜索。"
)

# 子智能体 2: 信息整理专家
summary_agent = create_agent(
    llm=llm,
    tools=[],
    system_prompt="你是信息整理专家。将搜索到的模型信息整理成清晰的报告。"
)

# 主智能体使用的工具
@tool
def search_ai_models(topic: str) -> str:
    """搜索 AI 模型，将任务委托给模型搜索专家"""
    result = model_search_agent.invoke({
        "messages": [{"role": "user", "content": f"搜索关于 {topic} 的模型"}]
    })
    return result["messages"][-1]["content"]

@tool
def summarize_report(data: str) -> str:
    """将搜索到的信息整理成报告"""
    result = summary_agent.invoke({
        "messages": [{"role": "user", "content": f"将以下信息整理成清晰的报告:\n{data}"}]
    })
    return result["messages"][-1]["content"]

# 主协调智能体
coordinator = create_agent(
    llm=llm,
    tools=[search_ai_models, summarize_report],
    system_prompt="""你是一个研究协调员。你的团队包括:
1. 模型搜索专家 - 搜索 AI 模型
2. 信息整理专家 - 整理报告

流程: 先搜索, 再整理。给出最终答案。"""
)

print("=" * 60)
print("子智能体模式 — 多模型搜索协作演示")
print("=" * 60)
print("\n[主协调智能体] 开始工作...")
print("  → 委托: 模型搜索专家 搜索最新 LLM 模型")
print("  → 委托: 信息整理专家 整理结果\n")

result = coordinator.invoke({
    "messages": [{"role": "user", "content": "搜索最新的 LLM 大语言模型，并整理成简洁报告"}]
})
print(f"最终结果:\n{result['messages'][-1]['content'][:500]}")
