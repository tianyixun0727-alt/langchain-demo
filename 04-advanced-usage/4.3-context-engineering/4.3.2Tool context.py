#!/usr/bin/env python3
"""上下文工程 Demo 2: 工具上下文 - 读写状态"""
#Tool 不仅能执行任务，还能通过 runtime.state 读写 Agent 的状态，并且配合 checkpointer 实现跨调用记忆。
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime#Tool 当前运行时环境
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver #短期记忆保存状态


# ---------- 1. 定义工具 ----------
@tool
def record_visit(runtime: ToolRuntime) -> Command:
    """
    记录访问次数，并更新状态。
    """
    # 从 State 中读取访问次数
    current = runtime.state.get("visit_count", 0)
    new_count = current + 1

    # 返回状态更新指令
    return Command(
        update={
            "visit_count": new_count,
            "messages": [
                {
                    "role": "tool",
                    "content": f"这是您第 {new_count} 次访问",
                    "tool_call_id": runtime.tool_call_id,
                }
            ],
        }
    )


# ---------- 2. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)


# ---------- 3. 创建 Checkpointer ----------
# 用于保存 Agent 状态
checkpointer = InMemorySaver()


# ---------- 4. 创建 Agent ----------
agent = create_agent(
    model=llm,
    tools=[record_visit],
    checkpointer=checkpointer,
)


# ---------- 5. 第一次调用 ----------
result1 = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "记录访问"}
        ]
    },
    config={
        "configurable": {
            "thread_id": "user-1"
        }
    }
)

print("第一次调用：")
print(result1["messages"][-1].content)


# ---------- 6. 第二次调用 ----------
result2 = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "再记录一次"}
        ]
    },
    config={
        "configurable": {
            "thread_id": "user-1"
        }
    }
)

print("第二次调用：")
print(result2["messages"][-1].content)


# ---------- 7. 第三次调用 ----------
result3 = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "继续记录"}
        ]
    },
    config={
        "configurable": {
            "thread_id": "user-1"
        }
    }
)

print("第三次调用：")
print(result3["messages"][-1].content)

#Tool 可以通过 runtime.state 读取和修改 Agent 的状态。
# 如果再配合 checkpointer 和 thread_id，这个状态还能跨多次调用保存下来，实现真正有记忆的 Agent。