#!/usr/bin/env python3
"""运行时系统 — 依赖注入（演示 runtime.context）"""

# ---------- 导入 ----------
from langchain.agents import create_agent          # 创建 Agent
from langchain.tools import tool, ToolRuntime     # tool 装饰器 + ToolRuntime 类型
from langchain_openai import ChatOpenAI           # 你的 DeepSeek 配置


# ---------- 模拟数据库类 ----------
class FakeDB:
    """一个假的数据库，仅用于演示"""
    def query(self, sql: str) -> str:
        return f"Executed: {sql}"


# ---------- 工具定义 ----------
@tool
def get_user_data(query: str, runtime: ToolRuntime) -> str:
    """
    在工具内部访问运行时上下文（数据库连接）。
    参数 runtime 由 LangChain 自动注入，无需手动传递。
    """
    # runtime.context 是调用时通过 context 参数传入的对象（这里是一个字典）
    db = runtime.context.get("database")   # 从上下文中取出数据库实例
    if db is None:
        return "错误：未找到数据库连接"
    # 执行查询并返回结果
    return db.query(f"SELECT * FROM users WHERE {query}")


# ---------- 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com",
    temperature=0,
)


# ---------- 创建 Agent ----------
agent = create_agent(
    llm=llm,
    tools=[get_user_data],
    system_prompt="你是一个数据助手，使用 get_user_data 工具查询用户信息。",
    # 注意：这里没有指定 context_schema，默认接受任意字典
)


# ---------- 调用 Agent ----------
# 通过 context 参数注入依赖（这里是数据库实例）
result = agent.invoke(
    {"messages": [{"role": "user", "content": "查询 id=1 的用户数据"}]},
    context={"database": FakeDB()}  
)

# 打印结果（取前100字符）
print(f"Runtime demo: {result['messages'][-1].content[:100]}")