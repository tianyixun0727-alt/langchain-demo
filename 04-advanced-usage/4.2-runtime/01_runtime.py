#!/usr/bin/env python3
"""运行时系统 — 依赖注入（演示 runtime.context）"""

# ---------- 导入 ----------
from langchain.agents import create_agent 
from langchain.tools import tool, ToolRuntime #Tool 的运行时环境对象
from langchain_openai import ChatOpenAI
# 新增导入（用于消除警告，但不使用 typing.Dict，直接用 dict）
# 无需额外导入


# ---------- 模拟数据库类 ----------
class FakeDB:
    """一个假的数据库，仅用于演示"""
    def query(self, sql: str) -> str:
        print(f"Executed: {sql}")
        return f"Executed: {sql}"
#不用mysql,模拟数据库对象,演示数据库对象如何被注入到 Tool 里面

# ---------- 工具定义（优化：参数名改为 condition，增强防御） ----------
@tool
def get_user_data(condition: str, runtime: ToolRuntime) -> str:
    """
    在工具内部访问运行时上下文（数据库连接）。
    参数 runtime 由 LangChain 自动注入，无需手动传递。
    condition: 可以是一个完整的 SQL 查询，或者 WHERE 子句的条件部分（不包含 WHERE 关键字），例如 "id = 1"。
    """
    # runtime.context 是调用时通过 context 参数传入的对象（这里是一个字典）
    db = runtime.context.get("database")   # 从上下文中取出数据库实例
    if db is None:
        return "错误：未找到数据库连接"
    # 防御：如果 condition 以 "SELECT" 开头，视为完整 SQL，直接使用
    if condition.strip().upper().startswith("SELECT"):
        sql = condition
    else:
        # 如果包含 WHERE 但不以 SELECT 开头，则视为条件部分已含 WHERE，直接拼接
        if "where" in condition.lower():
            sql = f"SELECT * FROM users {condition}"
        else:
            sql = f"SELECT * FROM users WHERE {condition}"
    # 执行查询并返回结果
    return db.query(sql)


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
    # 新增：显式指定上下文类型为 dict，消除 Pydantic 序列化警告（且不会导致类型错误）
    context_schema=dict,
)


# ---------- 调用 Agent ----------
# 通过 context 参数注入依赖（这里是数据库实例）
result = agent.invoke(
    {"messages": [{"role": "user", "content": "查询 id=1 的用户数据"}]},
    context={"database": FakeDB()}  
)

# 打印结果（取前100字符）
print(f"Runtime demo: {result['messages'][-1].content[:100]}")