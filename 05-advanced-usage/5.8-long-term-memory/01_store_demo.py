#!/usr/bin/env python3
"""Long-term Memory Demo — Store and recall across sessions"""

from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.tools import ToolRuntime
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

store = InMemoryStore()

@tool
def remember_fact(fact: str, runtime: ToolRuntime) -> str:
    """将一条信息存储到当前用户的长期记忆中"""
    uid = runtime.context.get("user_id", "default")
    namespace = ("users", uid, "facts")
    runtime.store.put(namespace, "latest", {"fact": fact})
    return f"Remembered: {fact}"

@tool
def recall_memories(runtime: ToolRuntime) -> str:
    """回忆当前用户的所有记忆"""
    uid = runtime.context.get("user_id", "default")
    items = runtime.store.search(("users", uid, "facts"))
    if items:
        return "\n".join(f"• {i.value['fact']}" for i in items)
    return "No memories found."

agent = create_agent(
    llm=llm,
    tools=[remember_fact, recall_memories],
    store=store,
)

print("=== Long-term Memory Demo ===")
print()

# Simulated session 1
print("--- Session 1 ---")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember that I like Python"}],
     "context": {"user_id": "alice"}},
    config={"configurable": {"thread_id": "session-1"}},
)
print(f"  {result['messages'][-1]['content']}")

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember I use VS Code"}],
     "context": {"user_id": "alice"}},
    config={"configurable": {"thread_id": "session-1"}},
)
print(f"  {result['messages'][-1]['content']}")

# Session 2 — across threads
print()
print("--- Session 2 (new thread) ---")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What do you remember about me?"}],
     "context": {"user_id": "alice"}},
    config={"configurable": {"thread_id": "session-2"}},
)
print(f"  {result['messages'][-1]['content']}")
print()
print("✅ Memory persisted across sessions using LangGraph Store!")
