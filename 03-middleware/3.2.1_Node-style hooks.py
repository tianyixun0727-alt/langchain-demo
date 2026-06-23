#!/usr/bin/env python3
"""自定义中间件示例：节点式钩子（日志记录）"""

from langchain.agents import create_agent
from langchain.agents.middleware import before_model, after_model# 导入节点式钩子装饰器
from langchain.agents.middleware.types import AgentState, Runtime# 导入 AgentState (当前 Agent 的“状态)和 Runtime 类型(当前执行环境)
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import Any, Optional # 导入 Any 和 Optional 类型，用于类型注解


# ---------- 工具定义 ----------
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city} 的天气晴朗，气温 25°C。"


# ---------- 节点式钩子 ----------
@before_model# 装饰器，表示这是一个在模型调用前执行的钩子函数
def log_before_model(state: AgentState, runtime: Runtime) -> Optional[dict[str, Any]]:# 定义一个函数，接受 AgentState 和 Runtime 作为参数，返回一个可选的字典（如果需要修改状态）
    """在每次模型调用前执行"""
    msg_count = len(state.get("messages", []))#统计当前对话轮数
    print(f"[BEFORE MODEL] 即将调用模型，当前消息数: {msg_count}")
    # 返回 None 表示不修改状态
    return None


@after_model# 装饰器，表示这是一个在模型调用后执行的钩子函数
def log_after_model(state: AgentState, runtime: Runtime) -> Optional[dict[str, Any]]:
    """在每次模型响应后执行"""
    last_msg = state["messages"][-1]
    content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
    print(f"[AFTER MODEL] 模型回复长度: {len(content)} 字符")
    print(f"[AFTER MODEL] 回复预览: {content[:50]}...")
    # 返回 None 表示不修改状态
    return None
#在模型输出之后，可以对结果做分析、日志或监控

# ---------- 初始化模型和 Agent ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

agent = create_agent(
    model=llm,
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