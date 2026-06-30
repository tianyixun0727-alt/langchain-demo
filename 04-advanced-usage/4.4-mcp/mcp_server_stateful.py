#!/usr/bin/env python3
"""MCP Demo 2b: 有状态会话服务器（SSE 网络版）"""

from fastmcp import FastMCP, Context

mcp = FastMCP("StatefulServer")

@mcp.tool()
async def increment_counter(ctx: Context) -> str:
    # 从会话状态中读取 counter（若不存在则返回 None）
    counter = await ctx.get_state("counter") or 0
    counter += 1
    await ctx.set_state("counter", counter)   # 键值对形式
    return f"计数器值: {counter}"

@mcp.tool()
async def get_counter(ctx: Context) -> str:
    counter = await ctx.get_state("counter") or 0
    return f"当前计数器值: {counter}"

if __name__ == "__main__":
    # 改为 SSE 传输，监听本地 8010 端口
    mcp.run(transport="sse", host="127.0.0.1", port=8010)