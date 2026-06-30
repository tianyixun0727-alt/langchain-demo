#基础 MCP — 服务端（SSE 网络版）

from fastmcp import FastMCP

mcp = FastMCP("MathServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b


if __name__ == "__main__":
    # 改为 SSE 传输，监听本地 8010 端口
    mcp.run(transport="sse", host="127.0.0.1", port=8010)