#前面的 Tool 都是独立函数,函数只能接收参数。
#但是在真实项目中，Tool 往往需要访问：数据库连接用户信息API Client配置文件
#如果不使用runtime，Tool 就无法访问这些外部资源（除非全局变量），导致代码耦合度高、难以测试和维护。
#所以 LangChain 提供了：runtime.context来实现依赖注入

#!/usr/bin/env python3
"""运行时系统 — 依赖注入（演示 runtime.context）"""

# ---------- 导入 ----------
from langchain.agents import create_agent 
from langchain.tools import tool, ToolRuntime #Tool 的运行时环境对象
from langchain_openai import ChatOpenAI


# ---------- 模拟数据库类 ----------
class FakeDB:
    """一个假的数据库，仅用于演示"""
    def query(self, sql: str) -> str:
        return f"Executed: {sql}"
#不用mysql,模拟数据库对象,演示数据库对象如何被注入到 Tool 里面

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
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)


# ---------- 创建 Agent ----------
agent = create_agent(
    model=llm,
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