#!/usr/bin/env python3
"""测试 —— LangSmith 评估"""

print("""
============================================
使用 LangSmith 测试智能体
============================================

你可以使用基于数据集的评估方式来测试智能体表现：

  import langsmith
  from langchain.agents import create_agent

  # 定义测试数据集
  dataset = [
      {"input": "巴黎的天气怎么样？", "expected": "晴天"},
      {"input": "把 hello 翻译成法语", "expected": "bonjour"},
  ]

  # 执行评估
  client = langsmith.Client()
  results = client.evaluate(
      lambda inputs: agent.invoke({
          "messages": [{
              "role": "user",
              "content": inputs["input"]
          }]
      }),
      data=dataset,
      evaluators=[...],
  )

测试策略：
  1. 正确性评估（Correctness Evaluation）
  2. 工具调用准确性跟踪（Tool-call Accuracy）
  3. 安全与护栏测试（Safety & Guardrails）
  4. 延迟性能测试（Latency Benchmarking）
  5. 回归测试（Regression Testing，对比历史基线）

============================================
""")