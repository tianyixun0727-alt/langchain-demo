#!/usr/bin/env python3
"""自定义中间件"""

from langchain.agents.middleware import middleware
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@middleware
class LogMiddleware:
    """在工具执行前记录所有工具调用"""
    
    async def before_tool_call(self, ctx, tool_call):
        print(f"[LOG] Calling tool: {tool_call.name}")
        print(f"[LOG] Args: {tool_call.args}")
        return tool_call

@tool
def simple_tool(msg: str) -> str:
    """一个简单的测试工具"""
    return f"Echo: {msg}"

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

agent = create_agent(
    llm=llm,
    tools=[simple_tool],
    middleware=[LogMiddleware()],
)

print("=== Custom Middleware Demo ===")
result = agent.invoke({
    "messages": [{"role": "user", "content": "Call simple_tool with 'hello'"}]
})
print(f"Result: {result['messages'][-1]['content'][:100]}")
