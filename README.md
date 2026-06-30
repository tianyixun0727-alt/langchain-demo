# LangChain Advanced Usage Guide

> 基于 [LangChain 官方文档](https://docs.langchain.com/oss/python/langchain) 整理的实战代码仓库。每个脚本均可独立运行，适合学习与演示。

## 目录结构

```
├── README.md
├── requirements.txt
│
├── 01-get-started/                        # 入门
│   ├── 1.1_install.py                     # 安装验证
│   ├── 1.2_quickstart.py                  # 第一个智能体
│   └── 1.3_philosophy.py                  # 设计哲学
│
├── 02-core-components/                    # 核心组件
│   ├── 2.1_models.py                      # 模型初始化与调用
│   ├── 2.2_messages.py                    # 消息体系（四类消息 + 工具调用流程）
│   ├── 2.3_tools.py                       # 工具定义（@tool 装饰器）
│   ├── 2.4_memory.py                      # 短期记忆（InMemorySaver）
│   ├── 2.5_event_streaming.py             # 事件流式输出
│   ├── 2.6_streaming.py                   # Token 流式输出
│   └── 2.7_structured output.py           # 结构化输出（Pydantic）
│
├── 03-middleware/                          # 中间件
│   ├── 3.1_prebuilt.py                    # 预置中间件：自动摘要
│   ├── 3.2.1_Node-style hooks.py          # 节点式钩子：日志记录
│   └── 3.2.2_Wrap-style hooks.py          # 包装式钩子：指数退避重试
│
├── 04-advanced-usage/                     # ⭐ 核心章节，高级功能
│   ├── 4.1-guardrails/                    # 安全机制
│   │   └── 01_guardrails.py               # PII 脱敏
│   ├── 4.2-runtime/                       # 运行时系统
│   │   └── 01_runtime.py                  # 依赖注入（runtime.context）
│   ├── 4.3-context-engineering/           # 上下文工程
│   │   ├── 4.3.1Model context.py          # 动态系统提示词
│   │   ├── 4.3.2Tool context.py           # 工具读写状态
│   │   └── 4.3.3Life-cycle Contex.py      # 生命周期自动摘要
│   ├── 4.4-mcp/                           # MCP 协议
│   │   ├── 4.4.1 mcp_client.py            # MCP 客户端
│   │   ├── math_server.py                 # MCP 服务端（数学工具）
│   │   ├── 4.4.2 mcp_client_stateful.py   # 有状态 MCP 客户端
│   │   └── mcp_server_stateful.py         # 有状态 MCP 服务端
│   ├── 4.5-hitl/                          # 人机协作
│   │   └── 4.5.1_hitl.py                  # 邮件发送审批
│   ├── 4.6-multi-agent/                   # 多智能体
│   │   ├── 4.6.1_overview.py              # 五种模式总览
│   │   ├── 4.6.2_subagents.py             # 子代理模式
│   │   ├── 4.6.3_handoffs.py              # 任务转交模式
│   │   ├── 4.6.4_skills.py                # 技能系统模式
│   │   ├── 4.6.5_router.py                # 路由器模式
│   │   └── 4.6.6_custom_workflow.py       # 自定义工作流（LangGraph）
│   ├── 4.7-rag/                           # 检索增强生成
│   │   ├── 4.7.1_2-Step RAG.py            # 基础 RAG
│   │   ├── 4.7.2_Agentic RAG.py           # Agent 自主决策 RAG
│   │   └── 4.7.3_Hybrid RAG.py            # 查询改写 + 重排序RAG
│   └── 4.8-long-term-memory/              # 长期记忆
│       └── 4.8.1_store_demo.py            # 跨会话记忆持久化
│
└── 05-test-deployment/                    # 测试与部署
│    ├── 5.1_testing.py                    # 五种测试策略
│    └── 5.2_evaluation_demo.py            # 评估系统 + 自动评分
│
└── 06-securities_qa                       # 法规证券问答
    ├── 《上市公司重大资产重组管理办法.docx  # 参考文件
    └── securities_agent.py                # 核心代码
```

## 快速开始

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境（Windows）
.venv\Scripts\Activate.ps1

# 安装依赖
uv pip install langchain langchain-openai langchain-core langgraph langchain-community openai tiktoken

# 运行第一个示例
python 01-get-started/1.2_quickstart.py
```

## 环境要求

- Python >= 3.9
- 模型 API Key（已预设 DeepSeek，通过内网 OpenAI 兼容 API 接入）

