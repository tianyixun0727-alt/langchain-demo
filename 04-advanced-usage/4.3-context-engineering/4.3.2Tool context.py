#!/usr/bin/env python3
"""上下文工程 Demo 2: 工具上下文 - 购物车管理（读写状态 + 静态配置）"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing import Annotated, NotRequired, List, Dict, Any
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain.tools import ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver


# ---------- 1. 扩展状态模式 ----------
class CartState(AgentState):
    cart: NotRequired[List[Dict[str, Any]]]   # 商品列表 [{"name": str, "price": float}]
    total: NotRequired[float]                 # 原价总额


# ---------- 2. 定义工具 ----------
@tool
def add_item(name: str, price: float, runtime: ToolRuntime) -> Command:
    """添加商品到购物车，并返回当前购物车摘要（含折扣后价格）。"""
    current_cart = runtime.state.get("cart", [])
    current_total = runtime.state.get("total", 0.0)

    new_item = {"name": name, "price": price}
    updated_cart = current_cart + [new_item]
    updated_total = current_total + price

    config = runtime.config or {}
    discount = config.get("configurable", {}).get("discount", 0.0)

    # 构建摘要
    item_list = ", ".join([f"{i['name']}(¥{i['price']:.1f})" for i in updated_cart])
    final_price = updated_total * (1 - discount)
    summary = f"购物车: {item_list} | 原价 ¥{updated_total:.1f}"
    if discount > 0:
        summary += f" → 折后 ¥{final_price:.1f} (折扣 {discount*100:.0f}%)"
    else:
        summary += f" | 实付 ¥{updated_total:.1f}"

    return Command(
        update={
            "cart": updated_cart,
            "total": updated_total,
            "messages": [
                ToolMessage(content=summary, tool_call_id=runtime.tool_call_id)
            ],
        }
    )


@tool
def clear_cart(runtime: ToolRuntime) -> Command:
    """清空购物车。"""
    return Command(
        update={
            "cart": [],
            "total": 0.0,
            "messages": [
                ToolMessage(content="购物车已清空", tool_call_id=runtime.tool_call_id)
            ],
        }
    )


# ---------- 3. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)


# ---------- 4. 创建 Checkpointer ----------
checkpointer = InMemorySaver()


# ---------- 5. 创建 Agent ----------
agent = create_agent(
    model=llm,
    tools=[add_item, clear_cart],
    state_schema=CartState,
    checkpointer=checkpointer,
)


# ---------- 6. 第一次调用 ----------
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "添加苹果，价格5.5"}]},
    config={"configurable": {"thread_id": "user-1"}},
)
print("第一次调用：")
print(result1["messages"][-1].content)


# ---------- 7. 第二次调用（启用10%折扣） ----------
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "添加香蕉，价格3.2"}]},
    config={"configurable": {"thread_id": "user-1", "discount": 0.1}},
)
print("第二次调用：")
print(result2["messages"][-1].content)


# ---------- 8. 第三次调用 ----------
result3 = agent.invoke(
    {"messages": [{"role": "user", "content": "添加橙子，价格4.0"}]},
    config={"configurable": {"thread_id": "user-1", "discount": 0.1}},
)
print("第三次调用：")
print(result3["messages"][-1].content)


# ---------- 9. 清空购物车 ----------
result4 = agent.invoke(
    {"messages": [{"role": "user", "content": "清空购物车"}]},
    config={"configurable": {"thread_id": "user-1", "discount": 0.1}},
)
print("清空后：")
print(result4["messages"][-1].content)