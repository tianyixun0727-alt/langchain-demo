#!/usr/bin/env python3
"""长期记忆演示 — 跨会话存储和回忆"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.tools import ToolRuntime
from langchain_openai import ChatOpenAI
from typing import TypedDict


llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
)

# 创建内存存储实例（模拟长期记忆数据库）
store = InMemoryStore()


# 定义上下文模式：告知 Agent 运行时会有 user_id 上下文
class UserContext(TypedDict):
    user_id: str


@tool
def remember_fact(fact: str, runtime: ToolRuntime) -> str:
    """将一条信息存储到当前用户的长期记忆中"""
    uid = runtime.context.get("user_id", "default") if runtime.context else "default"
    namespace = ("users", uid, "facts")
    # 用 fact 内容的哈希作为 key，避免覆盖之前的记忆
    key = f"fact_{abs(hash(fact)) % 10000}"
    runtime.store.put(namespace, key, {"fact": fact})
    return f"已记住：{fact}"


@tool
def recall_memories(runtime: ToolRuntime) -> str:
    """回忆当前用户的所有记忆"""
    uid = runtime.context.get("user_id", "default") if runtime.context else "default"
    items = runtime.store.search(("users", uid, "facts"))
    if items:
        return "\n".join(f"• {i.value['fact']}" for i in items)
    return "未找到任何记忆。"


# 创建智能体，注入存储实例和上下文模式
agent = create_agent(
    model=llm,
    tools=[remember_fact, recall_memories],
    store=store,
    context_schema=UserContext,
)

print("=== 长期记忆演示 ===")
print()

# 模拟第一次会话
print("--- 会话1 ---")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "记住我喜欢Python"}]},
    config={"configurable": {"thread_id": "session-1"}},
    context={"user_id": "alice"},  # context 作为 invoke 的独立参数传入
)
print(f"  {result['messages'][-1].content}")

result = agent.invoke(
    {"messages": [{"role": "user", "content": "记住我使用VS Code"}]},
    config={"configurable": {"thread_id": "session-1"}},
    context={"user_id": "alice"},
)
print(f"  {result['messages'][-1].content}")

# 第二次会话 — 新的线程，但相同用户
print()
print("--- 会话2 (新线程) ---")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "你还记得关于我的什么？"}]},
    config={"configurable": {"thread_id": "session-2"}},
    context={"user_id": "alice"},
)
print(f"  {result['messages'][-1].content}")
print()
print("使用 LangGraph Store 实现了跨会话的记忆持久化！")


# 要点：
# 1. context 通过 invoke(..., context={...}) 传入，不是放在 input dict 里
# 2. context_schema 告知 Agent 运行时会有什么上下文字段
# 3. store.put 的 key 要唯一（否则会覆盖），这里用哈希值区分
# 4. Store 跨 thread_id 持久化，Checkpointer 是同一 thread_id 内持久化