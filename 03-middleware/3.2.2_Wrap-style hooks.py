#!/usr/bin/env python3
"""自定义中间件示例：包装式钩子（带指数退避的重试）"""

import time
from typing import Callable
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
from langchain.agents.middleware.types import ModelRequest, ModelResponse
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# ---------- 工具定义 ----------
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city} 的天气晴朗，气温 25°C。"


# ---------- 包装式钩子：自动重试（指数退避） ----------
@wrap_model_call
def retry_with_backoff(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """
    模型调用失败时自动重试，每次重试等待时间翻倍（指数退避）
    """
    max_attempts = 3
    base_delay = 1  # 初始等待 1 秒

    for attempt in range(max_attempts):
        try:
            # 尝试执行真正的模型调用
            return handler(request)
        except Exception as e:
            # 如果是最后一次尝试，直接抛出异常
            if attempt == max_attempts - 1:
                print(f"❌ 重试 {max_attempts} 次均失败，最后错误: {e}")
                raise
            # 计算退避时间：1s, 2s, 4s, ...
            delay = base_delay * (2 ** attempt)
            print(f"⚠️ 模型调用失败 (尝试 {attempt + 1}/{max_attempts})，{delay}s 后重试... 错误: {e}")
            time.sleep(delay)
    # 理论上不会执行到这里，但为了类型检查保留
    raise RuntimeError("Unexpected end of retry loop")


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
    system_prompt="你是一个有用的天气助手。",
    middleware=[
        retry_with_backoff,  # 添加包装式中间件
    ],
)


# ---------- 运行测试 ----------
if __name__ == "__main__":
    print("=== 测试包装式钩子（带重试） ===\n")
    result = agent.invoke({
        "messages": [{"role": "user", "content": "今天上海的天气怎么样？"}]
    })
    print("\n=== 最终回答 ===")
    print(result["messages"][-1].content)