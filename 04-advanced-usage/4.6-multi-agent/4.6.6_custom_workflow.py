#!/usr/bin/env python3
"""自定义工作流 Demo：LangGraph 编排复杂流程"""

from langgraph.graph import StateGraph, END # LangGraph 是一个专门用于构建复杂工作流的库，StateGraph 是其中的核心类
from typing import TypedDict


# =========================================================
# 1️⃣ 定义状态（State）
# =========================================================

class GraphState(TypedDict):#定义“整个流程共享的数据结构”
    input: str#用户输入
    step: str#当前步骤
    output: str#最终输出结果

# =========================================================
# 2️⃣ 定义节点（Node）
# =========================================================

def classify(state: GraphState):
    """步骤1：分类用户输入"""
    text = state["input"] #从状态中读取用户输入

    if "天气" in text:
        return {"step": "weather"}
    elif "代码" in text:
        return {"step": "code"}
    else:
        return {"step": "general"}


def weather_node(state: GraphState):
    """天气处理节点"""
    return {"output": "今天晴天，适合出行 ☀️"}


def code_node(state: GraphState):
    """代码处理节点"""
    return {"output": "print('Hello World')"}


def general_node(state: GraphState):
    """通用处理节点"""
    return {"output": "我已经理解你的问题了。"}


# =========================================================
# 3️⃣ 构建 Graph
# =========================================================

graph = StateGraph(GraphState)

graph.add_node("classify", classify)
graph.add_node("weather", weather_node)
graph.add_node("code", code_node)
graph.add_node("general", general_node)
#将四个函数注册为图中的节点，并为每个节点赋予一个字符串名称

# =========================================================
# 4️⃣ 定义路由逻辑
# =========================================================

def router(state: GraphState):
    return state["step"]


graph.add_conditional_edges(
    "classify",
    router,
    {
        "weather": "weather",
        "code": "code",
        "general": "general",
    }
)


# =========================================================
# 5️⃣ 连接流程
# =========================================================

graph.set_entry_point("classify")

graph.add_edge("weather", END)
graph.add_edge("code", END)
graph.add_edge("general", END)


app = graph.compile()


# =========================================================
# 6️⃣ 运行测试
# =========================================================

print("\n===== 测试1 =====")
result1 = app.invoke({"input": "今天北京天气怎么样？"})
print(result1["output"])

print("\n===== 测试2 =====")
result2 = app.invoke({"input": "帮我写Python代码"})
print(result2["output"])

print("\n===== 测试3 =====")
result3 = app.invoke({"input": "随便聊聊"})
print(result3["output"])