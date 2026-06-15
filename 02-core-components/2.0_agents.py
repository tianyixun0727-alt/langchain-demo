#!/usr/bin/env python3
"""智能体详解 — Agent = Model + Harness 完整配置"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 共用模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

# =========================================================
# 1. 最小配置
# =========================================================
@tool
def get_time(city: str) -> str:
    """获取指定城市的当前时间"""
    return f"Current time in {city}: 12:00 PM"

print("=" * 60)
print("1. 最小智能体")
print("=" * 60)
agent_min = create_agent(llm=llm, tools=[get_time])
result = agent_min.invoke({
    "messages": [{"role": "user", "content": "What time is it in Tokyo?"}]
})
print(f"Output: {result['messages'][-1]}\n")


# =========================================================
# 2. 带系统提示词 + 结构化输出
# =========================================================
class WeatherInfo(BaseModel):
    city: str = Field(description="城市名")
    condition: str = Field(description="天气状况")
    temperature: str = Field(description="温度")

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气"""
    return f"Weather in {city}: Sunny, 25°C"

print("=" * 60)
print("2. 系统提示词 + 结构化输出")
print("=" * 60)
agent_with_schema = create_agent(
    llm=llm,
    tools=[get_weather],
    system_prompt="You are a weather assistant. Always provide structured weather data.",
    response_format=WeatherInfo,
    name="weather_agent",  # 多智能体系统中用作节点名
)
result = agent_with_schema.invoke({
    "messages": [{"role": "user", "content": "What's the weather in Beijing?"}]
})
parsed = result.get("structured_response")
if parsed:
    print(f"City: {parsed.city}")
    print(f"Condition: {parsed.condition}")
    print(f"Temperature: {parsed.temperature}")
print()


# =========================================================
# 3. 流式输出
# =========================================================
print("=" * 60)
print("3. 流式输出 (stream)")
print("=" * 60)
agent_stream = create_agent(llm=llm, tools=[])
for chunk in agent_stream.stream({
    "messages": [{"role": "user", "content": "Count from 1 to 3."}]
}):
    if msgs := chunk.get("messages"):
        last = msgs[-1]
        if isinstance(last, dict):
            print(last.get("content", ""), end="", flush=True)
print("\n")


# =========================================================
# 4. 配置执行环境
# =========================================================
print("=" * 60)
print("4. 执行环境配置")
print("=" * 60)
print("""
create_agent 支持以下执行环境配置:

  - max_turns: 最大工具调用轮数（防无限循环）
  - max_time: 单次调用最大执行时间
  - recursion_limit: 递归深度限制

示例:
  agent = create_agent(
      llm=llm,
      tools=[...],
      max_turns=10,
  )
""")


# =========================================================
# 5. 容错与重试
# =========================================================
print("=" * 60)
print("5. 容错机制")
print("=" * 60)
print(""+
  • 工具执行失败时，LangChain 会重试（可配置重试次数）
  • 使用中间件添加自定义重试、回退逻辑
  • 可通过 middleware 实现：
    - RetryMiddleware: 自动重试失败的工具调用
    - FallbackMiddleware: 当模型调用失败时回退到备选模型
    - TimeoutMiddleware: 超时控制
""")


if __name__ == "__main__":
    pass
