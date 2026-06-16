#!/usr/bin/env python3
"""LangSmith Overview — All capabilities"""

print("""
============================================
LangSmith — Observability & 调试
============================================

LangSmith provides deep visibility into agent behavior.

核心能力
----------------

1. 追踪
   Track every model call, tool execution, and state transition.
   All agent calls are automatically traced when enabled.

   export LANGSMITH_TRACING=true
   export LANGSMITH_API_KEY="lsv2_..."

2. 调试
   Visual interface to inspect:
   • Message histories
   • Tool inputs and outputs
   • Agent decisions at each step
   • Full agent loop step by step

3. 评估
   Run test datasets, compute metrics, track regressions.
   Compare different model configurations side by side.

   client = langsmith.Client()
   results = client.evaluate(
       lambda inputs: agent.invoke(inputs),
       data=dataset_name,
       evaluators=[correctness_evaluator],
   )

4. 监控
   • Real-time latency tracking
   • Token usage and cost monitoring
   • Error detection and alerting
   • Performance dashboards

5. LangSmith Engine
   Automatically monitors traces, detects anomalies,
   and proposes fixes without manual configuration.

快速开始
-----------
  export LANGSMITH_TRACING=true
  export LANGSMITH_API_KEY="lsv2_..."

  # All traces viewable at https://smith.langchain.com
""")
