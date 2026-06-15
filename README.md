# LangChain Advanced Usage Guide

> 基于 [LangChain 官方文档](https://docs.langchain.com/oss/python/langchain) 整理的实战代码仓库。每个脚本均可独立运行，适合学习与演示。

## 目录结构

```
├── README.md
├── requirements.txt
├── 01-get-started/                # 入门
│   ├── 01_install.py              # 安装验证
│   └── 02_quickstart.py           # 第一个智能体
├── 02-core-components/            # 核心组件
│   ├── 01_models.py               # 模型初始化
│   ├── 02_tools.py                # 工具定义
│   ├── 03_agents.py               # 智能体 + 结构化输出
│   ├── 04_memory.py               # 短期记忆
│   └── 05_streaming.py            # 流式输出
├── 03-middleware/                 # 中间件
│   ├── 01_prebuilt.py             # PII 检测
│   └── 02_custom.py               # 自定义中间件
├── 04-advanced-usage/             # ⭐ 核心章节
│   ├── 01_runtime.py              # 运行时系统
│   ├── 02_context_engineering.py  # 上下文工程
│   ├── 03_guardrails.py           # 安全机制
│   ├── 04-mcp/                    # MCP 协议 (小目录)
│   ├── 05_hitl.py                 # 人机协作
│   ├── 06-multi-agent/            # 多智能体 (小目录)
│   ├── 07-rag/                    # RAG (小目录)
│   ├── 08-long-term-memory/       # 长期记忆 (小目录)
│   ├── 09-patterns/               # 开发模式 (小目录)
│   └── 10-langsmith/              # LangSmith (小目录)
├── 05-test-deployment/            # 测试与部署
│   ├── 01_testing.py              # 测试策略
│   ├── 02_evaluation_demo.py      # 评估 demo
│   └── 03_deployment.py           # 部署选项
└── docs/                          # 文档
    ├── comparison_demo.py         # LangChain vs LangGraph vs MCP (可运行)
    └── comparison.md              # 完整对比表
```

## 快速开始

```bash
pip install -r requirements.txt
python 01-get-started/02_quickstart.py
```

## 环境要求

- Python >= 3.9
- 模型 API Key (已预设 DeepSeek)

## 演示路线

| 路径 | 适合人群 | 时长 |
|------|---------|------|
| `01-get-started/02_quickstart.py` | 首次接触 | 30s |
| `04-advanced-usage/01_runtime.py` | 核心概念 | 30s |
| `04-advanced-usage/04-mcp/01_overview.py` | MCP 协议 | 1min |
| `04-advanced-usage/06-multi-agent/02_subagents.py` | 多智能体 | 2min |
| `04-advanced-usage/07-rag/02_agentic_rag.py` | RAG | 2min |
| `05-test-deployment/02_evaluation_demo.py` | 测试评估 | 1min |
| `docs/comparison_demo.py` | 架构理解 | 1min |
