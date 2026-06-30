#!/usr/bin/env python3
"""MCP Demo 2b: 有状态会话客户端（使用 create_agent + session）"""

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
#python "04-advanced-usage/4.4-mcp/4.4.2 mcp_client_stateful.py"
async def main():
    # 1. 连接 SSE 服务
    client = MultiServerMCPClient({
        "stateful": {
            "transport": "sse",
            "url": "http://127.0.0.1:8010/sse",
        }
    })

    # 2. 使用 session 上下文（所有调用共享同一会话，状态累积）
    async with client.session("stateful") as session:
        tools = await load_mcp_tools(session)
        print(f"已加载工具: {[t.name for t in tools]}")

        # 3. 初始化 LLM
        llm = ChatOpenAI(
            model="deepseek-v3",
            api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
            base_url="http://10.187.126.181:3000/v1",
            temperature=0,
        )

        # 4. 创建智能体
        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt="你是一个计数器助手。"
        )

        # 5. 连续调用（状态在同一会话中持续）
        result1 = await agent.ainvoke({
            "messages": [{"role": "user", "content": "增加计数器"}]
        })
        print("第1次:", result1["messages"][-1].content)

        result2 = await agent.ainvoke({
            "messages": [{"role": "user", "content": "再增加一次"}]
        })
        print("第2次:", result2["messages"][-1].content)

        result3 = await agent.ainvoke({
            "messages": [{"role": "user", "content": "当前计数器是多少？"}]
        })
        print("第3次:", result3["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())