#!/usr/bin/env python3
"""LangChain 设计哲学 — Agent = Model + Harness"""

print("""
============================================
LangChain 设计哲学
============================================

LangChain 的核心信念:

  1. LLM 是强大的新技术
  2. 结合外部数据源时，LLM 更强大
  3. 未来的应用将越来越 "Agentic"（智能体化）
  4. 构建原型容易，构建生产级可靠的智能体仍然困难

两个核心关注点:
  1. 让开发者能够使用最好的模型
     不同提供商暴露不同的 API。标准化模型输入输出，
     让开发者可以轻松切换到最新的 SOTA 模型，避免锁定。

  2. 让模型能够编排与外部数据/计算交互的复杂流程
     模型不仅用于文本生成，还用于编排复杂的交互流程。
     LangChain 让定义工具、解析非结构化数据变得简单。

核心原则:
  • Agent = Model + Harness
    Harness 是模型循环之外的一切：提示词、工具、中间件
  • 可组合性 — 每个组件只负责一件事，自由组合
  • 提供商无关 — 标准化接口，无缝切换
  • 渐进式复杂度 — 从 create_agent 开始，逐步深入
  • 基于 LangGraph — 继承状态图的所有能力
  • 可观测性优先 — 内置 LangSmith 追踪

发展历史:
  2022-10 — v0.0.1 发布，LLM 抽象 + Chains
  2022-12 — 首个通用智能体（ReAct）
  2023-01 — OpenAI Chat Completion API / JS 版本发布
  2023-02 — LangChain + LangSmith + LangServe 三件套
  2025 — 新一代 create_agent + LangGraph 深度集成

决策指南:
  LangChain (create_agent) — 高度可定制，适合大多数场景
  Deep Agents — "电池内置"，内置上下文压缩、VFS、子智能体
  LangGraph — 底层编排框架，适合复杂工作流
  LangSmith — 追踪、调试、评估所有框架
============================================
""")

if __name__ == "__main__":
    pass
