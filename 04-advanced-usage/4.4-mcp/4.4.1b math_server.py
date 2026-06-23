#!/usr/bin/env python3
"""MCP Demo 1b: 自定义 MCP 服务器（数学工具）"""

from fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("MathServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    """两数相加"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """两数相乘"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """两数相除"""
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b

if __name__ == "__main__":
    # 通过 stdio 传输运行服务器
    mcp.run(transport="stdio")