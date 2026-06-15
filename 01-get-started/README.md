# 1. 入门指南

## 1.1 安装

```bash
pip install langchain
pip install "langchain[openai]"   # OpenAI 支持
pip install "langchain[anthropic]"  # Anthropic 支持
```

## 1.2 快速开始

运行 `python 02_quickstart.py` 创建第一个智能体。

## 设计理念

**Agent = Model + Harness** — 框架是模型循环之外的一切：提示词、工具、中间件。

核心原则：可组合性、提供商无关、渐进式复杂度、基于 LangGraph、可观测性优先。
