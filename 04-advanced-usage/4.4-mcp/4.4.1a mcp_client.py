#!/usr/bin/env python3
"""MCP Demo 1: 连接 MCP 服务器并使用工具"""
#安装依赖: pip install langchain-mcp-adapters fastmcp

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient# 导入 MultiServerMCPClient 类
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

async def main():
    # 1. 创建 MCP 客户端，连接本地 stdio 服务器
    client = MultiServerMCPClient({
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": ["math_server.py"],  # 假设 math_server.py 在同目录
        }
    })

    # 2. 获取服务器提供的所有工具
    tools = await client.get_tools()
    print(f"已加载工具: {[tool.name for tool in tools]}")

    # 3. 配置 LLM（使用 DeepSeek）
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key="sk-dac290dd70064370ac10057fdcee7f08",
        base_url="https://api.deepseek.com",
        temperature=0,
    )

    # 4. 创建 Agent，将 MCP 工具注入
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一个数学助手，使用提供的工具进行运算。"
    )

    # 5. 提问测试
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "计算 (3 + 5) × 12 的结果"}]
    })
    print("回答:", result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())