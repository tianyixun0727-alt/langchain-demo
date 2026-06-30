#!/usr/bin/env python3
"""MCP 智能体 - 使用数学工具（create_agent 风格）"""

import asyncio
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
#python "04-advanced-usage/4.4-mcp/4.4.1 mcp_client.py"
async def main():
    # 1. 连接 MCP SSE 服务
    client = MultiServerMCPClient({
        "remote_math": {
            "transport": "sse",
            "url": "http://127.0.0.1:8010/sse",
        }
    })
    tools = await client.get_tools()
    print("可用工具:", [t.name for t in tools])

    # 2. 初始化 LLM（您的内网地址）
    llm = ChatOpenAI(
        model="deepseek-v3",
        api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
        base_url="http://10.187.126.181:3000/v1",
        temperature=0,
    )

    # 3. 创建智能体（完全仿照您的示例）
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一个计数器助手。"
    )

    # 4. 执行查询（异步）
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "计算 (3+5)*12"}]
    })
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())