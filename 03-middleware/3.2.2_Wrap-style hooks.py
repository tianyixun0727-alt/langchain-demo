#!/usr/bin/env python3
"""自定义中间件示例：包装式钩子（带指数退避的重试）"""

import time
from typing import Callable
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call # 导入包装式钩子装饰器
from langchain.agents.middleware.types import ModelRequest, ModelResponse # 导入 ModelRequest 和 ModelResponse 类型，用于类型注解
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
            # 计算退避时间：1s, 2s, 4s, ...防止疯狂请求服务器,给服务器恢复时间
            delay = base_delay * (2 ** attempt)
            print(f"⚠️ 模型调用失败 (尝试 {attempt + 1}/{max_attempts})，{delay}s 后重试... 错误: {e}")
            time.sleep(delay)
    # 理论上不会执行到这里，但为了类型检查保留
    raise RuntimeError("Unexpected end of retry loop")


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
