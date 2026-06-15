#!/usr/bin/env python3
"""工具定义与使用"""

from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> list:
    """根据查询条件搜索数据库记录"""
    # 模拟数据库搜索
    results = [f"结果 {i}: 匹配到 {query}" for i in range(min(limit, 3))]
    return results if results else ["未找到结果。"]

# 查看工具的元数据信息
print(f"Tool name: {search_database.name}")
print(f"Tool description: {search_database.description}")
print(f"Tool args: {search_database.args}")

# 直接调用工具
result = search_database.invoke({"query": "LangChain", "limit": 5})
print(f"Search results: {result}")
