#!/usr/bin/env python3
"""技能模式 — 按需加载专业知识 + 实时调用对应网站"""

import requests
import json

print("=" * 60)
print("技能模式 — 按需加载专业知识 + 实时数据")
print("=" * 60)

# 技能库 + 对应的数据源
SKILL_CONFIG = {
    "python": {
        "name": "Python 技术",
        "description": "Python 编程、框架、库",
        "api_url": "https://pypi.org/pypi/{query}/json",
    },
    "ai_ml": {
        "name": "AI / 机器学习",
        "description": "LLM、深度学习、RAG",
        "api_url": None,  # 直接用 ModelScope
    },
    "devops": {
        "name": "DevOps",
        "description": "Docker、K8s、CI/CD",
        "api_url": "https://hub.docker.com/v2/repositories/{query}/",
    },
}

def detect_skills(query: str) -> list:
    q = query.lower()
    detected = []
    if any(kw in q for kw in ["python", "django", "flask", "pandas", "numpy", "pytorch"]):
        detected.append("python")
    if any(kw in q for kw in ["ai", "模型", "machine learning", "llm", "gpt", "rag", "大模型"]):
        detected.append("ai_ml")
    if any(kw in q for kw in ["docker", "deploy", "k8s", "kubernetes", "cicd"]):
        detected.append("devops")
    return detected

def fetch_pypi_info(package: str) -> str:
    """从 PyPI 获取包信息"""
    try:
        resp = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=10)
        data = resp.json()
        info = data["info"]
        return (
            f"📦 {info['name']} v{info.get('version','?')}\n"
            f"   描述: {info.get('summary','无')[:100]}\n"
            f"   作者: {info.get('author','未知')}\n"
            f"   许可证: {info.get('license','未知')}\n"
            f"   PyPI: https://pypi.org/project/{info['name']}/"
        )
    except Exception as e:
        return f"查询失败: {e}"

def fetch_modelscope_models(keyword: str) -> str:
    """从 ModelScope 获取模型信息"""
    try:
        resp = requests.get(
            f"https://modelscope.cn/api/v1/models?PageSize=3&Search={keyword}",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        models = resp.json().get("Data", {}).get("Models", [])
        if not models:
            return "未找到相关模型"
        results = []
        for m in models[:3]:
            results.append(f"🤖 {m.get('ModelName','?')} ({m.get('TaskName','通用')})")
        return "\n".join(results)
    except Exception as e:
        return f"查询失败: {e}"

skills = detect_skills("python requests 库的用法")
print(f"\n>>> 用户: python requests 库的用法")
print(f"   → 检测到技能: Python 技术")
print(f"   → 调用数据源: PyPI")
print(f"   → 获取数据中...\n")
print(fetch_pypi_info("requests"))
print()

skills = detect_skills("最新的大语言模型有哪些")
print(f">>> 用户: 最新的大语言模型有哪些")
print(f"   → 检测到技能: AI / 机器学习")
print(f"   → 调用数据源: ModelScope")
print(f"   → 获取数据中...\n")
print(fetch_modelscope_models("chat"))
print()

print("=" * 60)
print("技能模式工作原理")
print("=" * 60)
print("""
  用户提问
     ↓
  关键词检测 → 匹配技能
     ↓
  加载对应专业知识 + 调用对应数据源
     ├─ Python 问题 → PyPI + Python 技术栈知识
     ├─ AI 问题     → ModelScope + ML 知识
     └─ DevOps 问题 → Docker Hub + 部署知识
     ↓
  LLM 综合知识 + 实时数据 → 给出答案

  核心优势: 一个智能体，多种技能，按需切换。
""")
