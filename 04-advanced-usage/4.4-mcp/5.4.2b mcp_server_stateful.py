#!/usr/bin/env python3
"""MCP Demo 5a: 有状态会话服务器"""

from fastmcp import FastMCP, Context

mcp = FastMCP("StatefulServer")

@mcp.tool()
async def increment_counter(ctx: Context) -> str:
    """
    增加计数器并返回当前值。
    会话期间计数器会持续累加。
    """
    # 从会话状态中获取当前计数，默认为 0
    current = ctx.session_state.get("counter", 0) #类似字典,存放在 MCP 会话里
    current += 1
    # 更新会话状态
    ctx.session_state["counter"] = current  
    return f"计数器值: {current}"

@mcp.tool()
async def get_counter(ctx: Context) -> str:
    """获取当前计数器值"""
    current = ctx.session_state.get("counter", 0)
    return f"当前计数器值: {current}"

if __name__ == "__main__":
    mcp.run(transport="stdio")