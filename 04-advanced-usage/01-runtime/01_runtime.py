#!/usr/bin/env python3
"""运行时系统 — 依赖注入"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.runtime import ToolRuntime
from langchain_openai import ChatOpenAI


# Simulated database
class FakeDB:
    def query(self, sql): return f"Executed: {sql}"

@tool
def get_user_data(query: str, runtime: ToolRuntime) -> str:
    """在工具内部访问运行时上下文（数据库连接）"""
    db = runtime.context.get("database")
    return db.query(f"SELECT * FROM users WHERE {query}")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

agent = create_agent(
    llm=llm,
    tools=[get_user_data],
    system_prompt="You are a data assistant.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Query user data for id=1"}]},
    config={"context": {"database": FakeDB()}},
)
print(f"Runtime demo: {result['messages'][-1]['content'][:100]}")
