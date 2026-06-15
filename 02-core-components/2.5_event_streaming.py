#!/usr/bin/env python3
"""事件流 — Event Streaming (v3)"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

print("""
============================================
事件流 — Event Streaming (v3)
============================================

LangChain 支持 stream_events(..., version="v3") API，
返回带有类型化投影的 run 对象，每种投影可独立消费。

可用投影:

  stream.messages      模型消息流，每次 LLM 调用一个流
  ├── message.text     文本增量与最终文本
  ├── message.reasoning 推理内容增量（模型支持时）
  ├── message.tool_calls 工具调用参数块与最终结果
  └── message.output   模型调用完成后最终消息对象

  stream.values        智能体状态快照
  stream.output        最终智能体状态
  stream.subgraphs     嵌套图执行（子智能体）
  stream.tool_calls    工具执行生命周期（输入/输出增量/错误）
  stream.extensions    自定义转换器投影
============================================
""")

print("=== 基本示例: 消息流 ===")
agent = create_agent(
    llm=llm,
    tools=[],
    system_prompt="Be concise",
)

try:
    stream = agent.stream_events(
        {"messages": [{"role": "user", "content": "Count from 1 to 5."}]},
        version="v3",
    )
    for message in stream.messages:
        print(f"[{message.node}] ", end="", flush=True)
        for delta in message.text:
            print(delta, end="", flush=True)
except Exception as e:
    print(f"[注意] stream_events 需要 LangChain v3 版本支持: {e}")

print("\n\n=== 工具调用事件流 ===")
from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    """搜索网络信息"""
    return f"Results for: {query}"

agent_with_tools = create_agent(
    llm=llm,
    tools=[search_web],
    system_prompt="Be concise",
)

try:
    stream = agent_with_tools.stream_events(
        {"messages": [{"role": "user", "content": "Search for AI news"}]},
        version="v3",
    )
    # 读取最终输出
    final = stream.output
    print(f"Final state: {final}")
except Exception as e:
    print(f"[注意] stream_events 需要 LangChain v3 版本支持: {e}")
    print("使用传统 stream() 作为替代:")
    for chunk in agent_with_tools.stream({
        "messages": [{"role": "user", "content": "Say hello"}]
    }):
        if msgs := chunk.get("messages"):
            last = msgs[-1]
            if isinstance(last, dict):
                print(last.get("content", ""), end="", flush=True)
            else:
                print(last.content, end="", flush=True)
    print()


if __name__ == "__main__":
    pass
