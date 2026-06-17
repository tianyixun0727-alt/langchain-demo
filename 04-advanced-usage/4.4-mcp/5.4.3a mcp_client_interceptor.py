#!/usr/bin/env python3
"""MCP Demo 6b: 工具拦截器 - 客户端（日志 + 重试 + 上下文注入）"""
#在 AI 调用工具的过程中，加一层“中间处理层”

import asyncio
from dataclasses import dataclass
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.interceptors import MCPToolCallRequest
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.types import Command


# ---------- 1. 定义上下文 ----------
@dataclass
class UserContext:
    user_id: str
#把 user_id 绑定到整个 Agent 运行过程

# ---------- 2. 拦截器1：日志（记录 AI 调用了什么工具）----------
async def logging_interceptor(request: MCPToolCallRequest, handler):
    print(f"[LOG] 调用工具: {request.name}, 参数: {request.args}")
    result = await handler(request)
    print(f"[LOG] 工具返回: {str(result)[:50]}...")
    return result


# ---------- 3. 拦截器2：注入用户上下文(从运行环境中拿到 user_id，然后自动补到工具参数里) ----------
async def inject_user_context(request: MCPToolCallRequest, handler):
    # 从 runtime 中获取用户 ID
    user_id = request.runtime.context.user_id
    # 将 user_id 注入到工具参数中
    modified_request = request.override(
        args={**request.args, "user_id": user_id}
    )
    print(f"[CONTEXT] 注入用户ID: {user_id}")
    return await handler(modified_request)


# ---------- 4. 拦截器3：自动重试（指数退避）----------
async def retry_interceptor(request: MCPToolCallRequest, handler):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await handler(request)
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"[RETRY] 重试 {max_retries} 次失败: {e}")
                raise
            wait = 1 * (2 ** attempt)
            print(f"[RETRY] 第 {attempt+1} 次失败，{wait}s 后重试...")
            await asyncio.sleep(wait)


async def main():
    # 创建客户端，注册拦截器
    client = MultiServerMCPClient(
        {
            "order": {
                "transport": "stdio",
                "command": "python",
                "args": ["mcp_server_interceptor.py"],
            }
        },
        tool_interceptors=[
            logging_interceptor,          # 1. 日志
            inject_user_context,          # 2. 注入上下文
            retry_interceptor,            # 3. 重试
        ]
    )

    tools = await client.get_tools()
    print(f"已加载工具: {[t.name for t in tools]}\n")

    # 配置 LLM
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key="sk-dac290dd70064370ac10057fdcee7f08",
        base_url="https://api.deepseek.com",
        temperature=0,
    )

    # 创建 Agent，指定上下文结构
    agent = create_agent(
        model=llm,
        tools=tools,
        context_schema=UserContext,
        system_prompt="你是一个订单助手。"
    )

    # 调用时传入用户上下文
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "查询我的订单"}]},
        context=UserContext(user_id="user_123")
    )
    print("\n=== 最终回答 ===")
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())