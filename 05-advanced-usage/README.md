# 4. ⭐ 高级用法

生产级智能体工程核心章节。

| # | 路径 | 概念 | 形式 |
|---|------|------|------|
| 1 | `01_runtime.py` | 运行时系统 — 依赖注入 | 单文件 |
| 2 | `02_context_engineering.py` | 上下文工程 — 动态提示词 | 单文件 |
| 3 | `03_guardrails.py` | 安全机制 — PII / Guardrails | 单文件 |
| 4 | `04-mcp/` | **MCP 协议** — 连接外部工具 | 📂 子目录 |
| 5 | `05_hitl.py` | 人机协作 — 人工审批 | 单文件 |
| 6 | `06-multi-agent/` | **多智能体** — 5 种模式 | 📂 子目录 |
| 7 | `07-rag/` | **RAG** — 检索增强生成 | 📂 子目录 |
| 8 | `08-long-term-memory/` | **长期记忆** — LangGraph Store | 📂 子目录 |
| 9 | `09-patterns/` | **开发模式** — 6 种模式对比 | 📂 子目录 |
| 10 | `10-langsmith/` | **LangSmith** — 可观测性与评估 | 📂 子目录 |
| 11 | `11-observability/` | **可观测性** — LangSmith 追踪设置 | 📂 子目录 |
| 12 | `12-frontend/` | **前端支持** — Frontend SDK & Agent Chat UI | 📂 子目录 |

## 演示路线

```bash
# 快速了解 (每个 < 30秒)
python 01-runtime/01_runtime.py
python 03-guardrails/03_guardrails.py
python 05-hitl/05_hitl.py

# 子目录 (每个目录下都有 README)
python 04-mcp/01_overview.py
python 06-multi-agent/02_subagents.py
python 07-rag/02_agentic_rag.py

# 生产级应用
python 08-long-term-memory/02_store_demo.py
python 10-langsmith/02_tracing_demo.py

# 新增章节
python 11-observability/01_overview.py
python 12-frontend/01_overview.py
```
