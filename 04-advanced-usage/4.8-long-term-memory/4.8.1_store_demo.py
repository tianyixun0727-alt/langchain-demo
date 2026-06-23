#!/usr/bin/env python3
"""长期记忆演示 — 跨会话存储和回忆"""

from langgraph.store.memory import InMemoryStore  # 导入内存存储，用于保存长期记忆
from langchain.agents import create_agent         # 导入创建智能体的函数
from langchain.tools import tool                  # 导入工具装饰器
from langchain.tools import ToolRuntime           # 工具运行时环境，提供上下文和存储访问
from langchain_openai import ChatOpenAI           # 导入OpenAI兼容的聊天模型

# 配置大语言模型（使用DeepSeek）
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
)

# 创建内存存储实例（模拟长期记忆数据库）
store = InMemoryStore()

@tool
def remember_fact(fact: str, runtime: ToolRuntime) -> str:
    """将一条信息存储到当前用户的长期记忆中"""
    # 从运行时上下文中获取用户ID，如果不存在则使用"default"
    uid = runtime.context.get("user_id", "default")
    # 构造命名空间：按用户隔离记忆
    namespace = ("users", uid, "facts")
    # 将事实存入存储，键名为"latest"（每次覆盖最新一条）
    runtime.store.put(namespace, "latest", {"fact": fact})
    return f"已记住：{fact}"

@tool
def recall_memories(runtime: ToolRuntime) -> str:
    """回忆当前用户的所有记忆"""
    uid = runtime.context.get("user_id", "default")
    # 搜索该用户命名空间下的所有记忆条目
    items = runtime.store.search(("users", uid, "facts"))
    if items:
        # 格式化输出所有记忆内容
        return "\n".join(f"• {i.value['fact']}" for i in items)
    return "未找到任何记忆。"

# 创建智能体，并注入存储实例
agent = create_agent(
    model=llm,
    tools=[remember_fact, recall_memories],  # 注册记忆工具
    store=store,                             # 注入存储，让工具可以访问
)

print("=== 长期记忆演示 ===")
print()

# 模拟第一次会话
print("--- 会话1 ---")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "记住我喜欢Python"}],
     "context": {"user_id": "alice"}},  # 指定用户ID
    config={"configurable": {"thread_id": "session-1"}},  # 会话线程ID
)
print(f"  {result['messages'][-1]['content']}")

result = agent.invoke(
    {"messages": [{"role": "user", "content": "记住我使用VS Code"}],
     "context": {"user_id": "alice"}},
    config={"configurable": {"thread_id": "session-1"}},
)
print(f"  {result['messages'][-1]['content']}")

# 第二次会话 — 新的线程，但相同用户
print()
print("--- 会话2 (新线程) ---")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "你还记得关于我的什么？"}],
     "context": {"user_id": "alice"}},
    config={"configurable": {"thread_id": "session-2"}},  # 不同的thread_id
)
print(f"  {result['messages'][-1]['content']}")
print()
print("✅ 使用LangGraph Store实现了跨会话的记忆持久化！")