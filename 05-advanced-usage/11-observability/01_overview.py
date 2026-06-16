#!/usr/bin/env python3
"""可观测性 — LangSmith Tracing"""

print("""
============================================
可观测性 — Observability
============================================

LangChain 智能体通过 LangSmith 自动支持追踪。
追踪记录执行中的每一步：从用户输入到最终响应，
包括所有工具调用、模型交互和决策点。

前提条件:
  1. LangSmith 账号: smith.langchain.com
  2. LangSmith API Key
  3. 设置环境变量:
     export LANGSMITH_TRACING=true
     export LANGSMITH_API_KEY="lsv2_..."

使用示例:
  from langchain.agents import create_agent

  agent = create_agent(llm=llm, tools=[...])
  # 所有调用自动追踪，无需额外代码
  response = agent.invoke({...})

选择性追踪:
  import langsmith as ls

  # 仅追踪此调用
  with ls.tracing_context(enabled=True):
      agent.invoke({...})

  # 此调用不会被追踪（如果 LANGSMITH_TRACING 未设置）
  agent.invoke({...})

记录到特定项目:
  import os
  os.environ["LANGCHAIN_PROJECT"] = "my-agent-project"

添加元数据:
  response = agent.invoke(
      {"messages": [...]},
      config={"run_name": "my-run", "tags": ["production", "v2"]}
  )

可观测性的价值:
  * 调试 --- 查看完整执行轨迹，定位失败点
  * 评估 --- 比较不同版本的智能体表现
  * 监控 --- 生产环境中追踪延迟、错误率
  * 审计 --- 记录所有决策过程，满足合规要求
============================================
""")

# 如果已配置环境变量，可运行追踪示例
import os

if os.environ.get("LANGSMITH_TRACING") == "true":
    from langchain.agents import create_agent
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key="sk-dac290dd70064370ac10057fdcee7f08",
        base_url="https://api.deepseek.com"
    )

    agent = create_agent(
        llm=llm,
        tools=[],
        system_prompt="You are a helpful assistant.",
    )

    result = agent.invoke({
        "messages": [{"role": "user", "content": "Hello! What can you do?"}]
    })
    print(f"Agent response: {result['messages'][-1]}")
else:
    print("\n[提示] 设置 LANGSMITH_TRACING=true 和 LANGSMITH_API_KEY 后可运行追踪示例")

if __name__ == "__main__":
    pass
