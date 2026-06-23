#!/usr/bin/env python3
"""MCP Demo 2a: 有状态会话客"""
#MCP 不仅能提供工具，还能保存会话状态   
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
#将工具绑定到指定的会话上，让工具执行时使用该会话，而不是每次都新建
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

async def main():#创建 MCP 客户端，连接本地 stdio 服务器
    client = MultiServerMCPClient({
        "stateful": {
            "transport": "stdio",
            "command": "python",
            "args": ["mcp_server_stateful.py"],
        }
    })

    # 创建持久会话（会话期间状态保持）创建了一个真正的 MCP Session,后面对话全保存在里面
    async with client.session("stateful") as session:
        # 通过会话加载工具
        tools = await load_mcp_tools(session)
        print(f"已加载工具: {[t.name for t in tools]}")

        # 配置 LLM
        llm = ChatOpenAI(
            model="deepseek-v3",
            api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
            base_url="http://10.187.126.181:3000/v1",
            temperature=0,
        )

        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt="你是一个计数器助手。"
        )

        # 第一次调用：增加计数器
        result1 = await agent.ainvoke({
            "messages": [{"role": "user", "content": "增加计数器"}]
        })
        print("第1次:", result1["messages"][-1].content)

        # 第二次调用：再次增加
        result2 = await agent.ainvoke({
            "messages": [{"role": "user", "content": "再增加一次"}]
        })
        print("第2次:", result2["messages"][-1].content)

        # 第三次调用：查询当前值
        result3 = await agent.ainvoke({
            "messages": [{"role": "user", "content": "当前计数器是多少？"}]
        })
        print("第3次:", result3["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())