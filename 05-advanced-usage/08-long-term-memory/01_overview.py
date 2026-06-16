#!/usr/bin/env python3
"""Long-term Memory — Concepts and Architecture"""

print("""
============================================
Long-term Memory — Overview
============================================

Unlike short-term memory (which is scoped to a single thread),
long-term memory persists across threads and can be recalled
at any time, across different conversations.

基于 LangGraph Store 构建
-------------------------
Long-term memories are saved as JSON documents organized by:
  • Namespace — like a folder (e.g., ("users", user_id, "facts"))
  • Key — like a file name (e.g., "latest", "preferences")
  • Value — the actual JSON data

记忆类型
------------
  1. Semantic Memory
     Facts and concepts about the world.
     Example: "The user prefers Python over JavaScript."

  2. Episodic Memory
     Past interactions and experiences.
     Example: "The user asked about RAG in the last session."

  3. Procedural Memory
     How to do things — skills, workflows, preferences.
     Example: "Always provide code examples with explanations."

Storage Backends
----------------
  InMemoryStore (prototyping):
    from langgraph.store.memory import InMemoryStore
    store = InMemoryStore()

  PostgreSQL (production):
    from langgraph.store.postgres import PostgresStore
    with PostgresStore.from_conn_string(DB_URI) as store:
        ...

Usage in Tools
--------------
  @tool
  def remember(fact: str, runtime: ToolRuntime) -> str:
      uid = runtime.context["user_id"]
      runtime.store.put(("users", uid, "facts"), "latest", {"fact": fact})
      return f"Remembered: {fact}"

  @tool
  def recall(runtime: ToolRuntime) -> str:
      items = runtime.store.search(("users", uid, "facts"))
      return "\\n".join(i.value["fact"] for i in items)

See: 02_store_demo.py for a runnable example.
""")
