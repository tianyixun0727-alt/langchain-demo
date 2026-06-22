#!/usr/bin/env python3
"""工具定义与使用"""

from langchain.tools import tool

@tool#使用了 LangChain 提供的 @tool 装饰器
def search_database(query: str, limit: int = 10) -> list:
    """根据查询条件搜索数据库记录"""
    # 模拟数据库搜索
    results = [f"结果 {i}: 匹配到 {query}" for i in range(min(limit, 3))]
    return results if results else ["未找到结果。"]

# Tool 被装饰之后，LangChain 自动帮我们生成的三种元信息
print(f"Tool name: {search_database.name}")#用于 LLM 识别工具
print(f"Tool description: {search_database.description}")#告诉模型这个工具是做什么的
print(f"Tool args: {search_database.args}")#告诉模型这个工具需要什么输入

# 直接调用工具
result = search_database.invoke({"query": "LangChain", "limit": 5})
print(f"Search results: {result}")
