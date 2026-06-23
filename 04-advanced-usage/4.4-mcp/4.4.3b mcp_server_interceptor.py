#!/usr/bin/env python3
"""MCP Demo 3b: 工具拦截器 - 服务端"""

from fastmcp import FastMCP

mcp = FastMCP("OrderServer")

# 模拟订单数据库
ORDERS = {
    "user_123": ["订单A（已发货）", "订单B（处理中）"],
    "user_456": ["订单C（已送达）"],
}

@mcp.tool()
def search_orders(user_id: str) -> str:
    """根据用户ID查询订单"""
    orders = ORDERS.get(user_id, [])
    if orders:
        return f"找到 {len(orders)} 个订单: {', '.join(orders)}"
    return "未找到订单"

@mcp.tool()
def submit_order(product: str, user_id: str) -> str:
    """提交新订单"""
    return f"订单已提交: {product} (用户: {user_id})"

if __name__ == "__main__":
    mcp.run(transport="stdio")