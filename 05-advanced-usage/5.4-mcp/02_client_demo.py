#!/usr/bin/env python3
"""MCP 客户端演示 — 调用真实外部 API（模型搜索）"""

import requests
import json

print("=" * 60)
print("MCP 协议演示 — 调用外部 API")
print("=" * 60)

# 定义 MCP 工具函数（模拟 MCP Server 提供的工具）
def modelscope_search(keyword="chat"):
    """搜索 ModelScope 上的模型"""
    url = f"https://modelscope.cn/api/v1/models?PageSize=3&Sort=GmtCreate&Search={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            models = data.get("Data", {}).get("Models", [])
            results = []
            for m in models[:3]:
                name = m.get("ModelName", m.get("Name", "未知"))
                task = m.get("TaskName", "通用")
                likes = m.get("LikeCount", 0)
                results.append(f"  • {name} (任务: {task}, 👍 {likes})")
            return "\n".join(results)
        return f"请求失败: HTTP {resp.status_code}"
    except Exception as e:
        return f"连接错误: {e}"

def huggingface_search(query="llm"):
    """搜索 HuggingFace 上的热门模型"""
    url = f"https://huggingface.co/api/models?search={query}&sort=downloads&direction=-1&limit=3"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            models = resp.json()
            results = []
            for m in models[:3]:
                model_id = m.get("modelId", "未知")
                downloads = m.get("downloads", 0)
                pipeline = m.get("pipeline_tag", "其他")
                results.append(f"  • {model_id} (类型: {pipeline}, 下载: {downloads:,})")
            return "\n".join(results)
        return f"请求失败: HTTP {resp.status_code}"
    except Exception as e:
        return f"连接错误: {e}"

def get_weather(city="北京"):
    """通过 wttr.in 获取天气"""
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=%C+%t+%w", timeout=10)
        if resp.status_code == 200:
            return f"{city} 天气: {resp.text.strip()}"
        return f"查询失败: HTTP {resp.status_code}"
    except Exception as e:
        return f"连接错误: {e}"

print("\n📡 正在连接外部数据源...\n")

# 演示 1: 搜索 ModelScope
print(">>> MCP 工具: modelscope_search('chat')")
result = modelscope_search("chat")
print(result)
print()

# 演示 2: 搜索 HuggingFace
print(">>> MCP 工具: huggingface_search('llm')")
result = huggingface_search("llm")
print(result)
print()

# 演示 3: 查询天气
print(">>> MCP 工具: get_weather('北京')")
result = get_weather("北京")
print(result)
print()

print("=" * 60)
print("MCP 工作原理")
print("=" * 60)
print("""
在 MCP 架构中，这些工具函数通过 MCP Server 暴露：

  LangChain Agent ──MCP协议──→ MCP Server ──→ 外部 API
                                         │
                                         ├── modelscope.cn
                                         ├── huggingface.co
                                         └── wttr.in

实际用法：
  from langchain.mcp import MCPTool
  from langchain.agents import create_agent

  # 连接到 MCP Server
  mcp_tools = MCPTool.from_server("http://localhost:8000/mcp")
  
  # 创建智能体
  agent = create_agent(llm=llm, tools=[*mcp_tools])
""")
