#!/usr/bin/env python3
"""MCP Demo 5b: 有状态会话客户端"""

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
#load_mcp_tools 的作用就是：将工具绑定到指定的会话上，让工具执行时使用该会话，而不是每次都新建
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

async def main():
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
            model="deepseek-chat",
            api_key="sk-dac290dd70064370ac10057fdcee7f08",
            base_url="https://api.deepseek.com",
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