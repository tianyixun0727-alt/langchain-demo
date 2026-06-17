#!/usr/bin/env python3
"""上下文工程 Demo 2: 工具上下文 - 读写状态"""

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI
from langgraph.types import Command  # 用于返回状态更新指令


# ---------- 1. 定义工具 ----------
@tool
def record_visit(runtime: ToolRuntime) -> str:
    """
    记录访问次数：每次调用将状态中的 visit_count 加 1，并返回当前次数。
    """
    # 从 state 中读取当前访问次数，默认为 0
    current = runtime.state.get("visit_count", 0)
    new_count = current + 1

    # 返回 Command 更新状态，同时向用户回复当前次数
    return Command(
        update={"visit_count": new_count},          # 更新状态字段
        # 注意：工具返回内容需要作为 ToolMessage 追加，这里通过返回值自动处理
        # 但 Command 会取代工具返回值，需放在 graph 中处理。
        # 为了简单，我们直接在返回值中返回文本，并单独更新状态。
    )

# 但由于 Command 会取代工具的字符串返回值，我们需要调整写法：
# 更好的方式：先返回消息，再更新状态。但简单起见，我们可以在工具中不返回 Command，
# 而是直接返回字符串，然后通过 after_model 钩子更新？不，文档建议工具返回 Command 来更新状态。
# 但工具返回 Command 后，Agent 会将 Command 应用到状态，但工具的原始输出会丢失吗？
# 实际上，工具若返回 Command，则 Command 中的 update 会合并到状态，但工具的输出（ToolMessage）仍会追加。
# 但 Command 不能同时包含文本输出，我们需要在 Command 中指定 messages 字段来添加 ToolMessage。

# 重写工具，在 Command 中同时添加消息和状态更新：
@tool
def record_visit_v2(runtime: ToolRuntime) -> Command:
    """记录访问次数，并返回当前次数"""
    current = runtime.state.get("visit_count", 0)
    new_count = current + 1
    return Command(
        update={
            "visit_count": new_count,
            "messages": [  # 追加一条 ToolMessage，内容为回复给用户的信息
                {"role": "tool", "content": f"这是您第 {new_count} 次访问", "tool_call_id": runtime.tool_call_id}
            ]
        }
    )

# 我们采用第二种写法，更规范。


# ---------- 2. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com",
    temperature=0,
)


# ---------- 3. 创建 Agent ----------
agent = create_agent(
    model=llm,
    tools=[record_visit_v2],
)


# ---------- 4. 调用测试 ----------
# 第一次调用，状态中无 visit_count，工具会初始化为 0 → 1
result1 = agent.invoke({
    "messages": [{"role": "user", "content": "记录访问"}]
})
print("第一次调用回复:", result1["messages"][-1].content)

# 第二次调用，状态中已有 visit_count=1，会变为 2
result2 = agent.invoke({
    "messages": [{"role": "user", "content": "再记录一次"}]
})
print("第二次调用回复:", result2["messages"][-1].content)