#!/usr/bin/env python3
"""中间件概览 — 在智能体循环中注入自定义逻辑"""

print("""
============================================
中间件 — Middleware 概览
============================================

中间件提供在模型调用和工具执行前后插入钩子的能力。

用途:
  • 追踪 — 日志、分析、调试
  • 转换 — 提示词变换、工具选择、输出格式化
  • 韧性 — 重试、回退、提前终止
  • 安全 — 速率限制、护栏、PII 检测

使用方法:
  from langchain.agents import create_agent
  from langchain.agents.middleware import SummarizationMiddleware

  agent = create_agent(
      llm=llm,
      tools=[...],
      middleware=[
          SummarizationMiddleware(...),
          HumanInTheLoopMiddleware(...),
      ],
  )

智能体循环中的钩子点:

  用户输入
     ↓
  [Pre-model hook] — 模型调用前注入
     ↓
  调用模型
     ↓
  [Post-model hook] — 处理模型输出
     ↓
  是否需要调用工具? ──是──→ [Pre-tool hook] → 执行工具 → [Post-tool hook] → (回到预模型钩子)
     ↓ 否
   [Post-agent hook] — 最终输出处理
     ↓
  返回结果

中间件继承 LangGraph 上下文:
  将 create_agent 放入更大的 StateGraph 时，
  所有中间件钩子继续正常运行。

预置中间件:
  • PIIFilterMiddleware — 输入/输出中的 PII 检测与脱敏
  • HumanInTheLoopMiddleware — 人工审批特定工具调用
  • SummarizationMiddleware — 自动总结长对话历史
  • RetryMiddleware — 工具调用失败自动重试
  • TimeoutMiddleware — 超时控制
  • LoggingMiddleware — 日志记录
============================================
""")

if __name__ == "__main__":
    pass
