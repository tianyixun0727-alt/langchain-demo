#!/usr/bin/env python3
"""Deep Agents — 全能型智能体演示"""

import requests

print("=" * 60)
print("Deep Agents 演示 — 全能型智能体")
print("=" * 60)
print("""
Deep Agents 是建立在 LangChain 之上的高级智能体框架，
内置了常用的能力:

  • 自动上下文压缩 — 处理超长对话
  • 虚拟文件系统 — 读写和管理文件
  • 规划能力 — 自动分解复杂任务
  • 子智能体 — 按需生成专用子智能体
  • 上下文管理 — 智能管理记忆

安装:
  pip install deepagents

用法:
  from deepagents import create_deep_agent
  
  agent = create_deep_agent(
      llm=llm,
      tools=[...],
      system_prompt="你是一个全能助手"
  )
  
  result = agent.invoke({
      "messages": [{"role": "user", "content": "..."}]
  })
""")

# 演示: 用 requests 模拟 Deep Agents 的上下文压缩功能
print("演示: 模拟 Deep Agents 上下文压缩")
print("-" * 50)

# 模拟一个长对话
long_conversation = [
    "我的名字是张三",
    "我是一名 Python 开发者",
    "我擅长 FastAPI 和 PostgreSQL",
    "最近在学习大语言模型相关的技术",
    "我住在北京",
    "我的公司是做 AI 应用的",
    "我喜欢在周末写开源项目",
]

print("原始对话历史:")
for i, msg in enumerate(long_conversation, 1):
    print(f"  {i}. {msg}")

# 模拟上下文压缩
compressed = {
    "用户信息": {
        "name": "张三",
        "role": "Python 开发者",
        "skills": ["FastAPI", "PostgreSQL", "LLM"],
        "location": "北京",
        "company_type": "AI 应用",
        "interests": ["开源项目"],
    },
    "最近活跃的消息数": len(long_conversation),
}

print(f"\n压缩后 ({len(json.dumps(compressed, ensure_ascii=False))} 字符):")
print(f"  {json.dumps(compressed, ensure_ascii=False, indent=2)}")
print()

# 演示: 实时搜索 GitHub
print("演示: 模拟 Deep Agents 的规划 + 搜索能力")
print("-" * 50)
print("任务: 了解 LangChain 最新动态")
print()

print("🤖 Deep Agent 开始规划...")
plan = [
    "1. 搜索 GitHub 上 LangChain 热门仓库",
    "2. 获取仓库关键信息",
    "3. 整理报告",
]
for step in plan:
    print(f"  {step}")

try:
    resp = requests.get(
        "https://api.github.com/search/repositories?q=langchain&sort=stars&per_page=5",
        headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )
    repos = resp.json().get("items", [])
    print("\n📊 搜索结果:")
    for r in repos:
        print(f"  • {r['full_name']} ⭐{r['stargazers_count']}")
        print(f"    {r.get('description','')[:80]}")
except Exception as e:
    print(f"  搜索失败: {e}")

print()
print("=" * 60)
print("何时使用 Deep Agents")
print("=" * 60)
print("""
  ✅ 需要最大能力且最少配置
  ✅ 任务涉及多步骤规划和执行
  ✅ 需要内置的上下文管理
  ✅ 需要子智能体能力

  ❌ 需要精细控制每个组件 → 用 LangChain Agents
  ❌ 任务非常简单 → 直接用单个 Agent
""")
