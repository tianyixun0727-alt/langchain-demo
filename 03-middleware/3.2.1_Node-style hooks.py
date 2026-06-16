#!/usr/bin/env python3
"""自定义中间件示例：节点式钩子（日志记录）"""

from langchain.agents import create_agent
from langchain.agents.middleware import before_model, after_model
from langchain.agents.middleware.types import AgentState, Runtime
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import Any, Optional


# ---------- 工具定义 ----------
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city} 的天气晴朗，气温 25°C。"


# ---------- 节点式钩子 ----------
@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> Optional[dict[str, Any]]:
    """在每次模型调用前执行"""
    msg_count = len(state.get("messages", []))
    print(f"[BEFORE MODEL] 即将调用模型，当前消息数: {msg_count}")
    # 返回 None 表示不修改状态
    return None


@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> Optional[dict[str, Any]]:
    """在每次模型响应后执行"""
    last_msg = state["messages"][-1]
    content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
    print(f"[AFTER MODEL] 模型回复长度: {len(content)} 字符")
    print(f"[AFTER MODEL] 回复预览: {content[:50]}...")
    # 返回 None 表示不修改状态
    return None


# ---------- 初始化模型和 Agent ----------
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com",
    temperature=0,
)

agent = create_agent(
    llm=llm,
    tools=[get_weather],
    system_prompt="你是一个有帮助的天气助手。",
    middleware=[
        log_before_model,
        log_after_model,
    ],
)


# ---------- 运行测试 ----------
if __name__ == "__main__":
    print("=== 开始测试节点式钩子 ===\n")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": "今天北京天气怎么样？"}]
    })
    
    print("\n=== 最终回答 ===")
    print(result["messages"][-1].content)