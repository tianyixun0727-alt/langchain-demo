# 11. 可观测性 — Observability (LangSmith)

## 概述

通过 LangSmith 追踪获取智能体行为的深度可见性。

## 文件说明

| File | Description |
|------|-------------|
| `01_overview.py` | 可观测性设置与用法 |

## 快速开始

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="lsv2_..."
```

## 能力

- **实时追踪** — 查看每次模型调用、工具执行、状态转换
- **选择性追踪** — 通过 tracing_context 控制追踪范围
- **元数据标注** — 为追踪添加自定义标签和元数据
- **项目隔离** — 将追踪记录到不同项目
- **性能监控** — 延迟、错误率、使用量
- **可观测性** 与 **LangSmith** — 追踪覆盖 10-langsmith 的评估能力
