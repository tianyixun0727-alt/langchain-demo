#!/usr/bin/env python3
"""部署选项概览"""

print("""
============================================
部署方式（Deployment Options）
============================================

1. LangGraph Server
   托管式部署，支持自动扩缩容，并内置 API 接口。
   部署命令：
   langsmith deploy --agent agent.py

2. Docker 容器部署
   在任意云平台进行容器化部署。

   构建镜像：
   langsmith build -t my-agent:latest

   运行容器：
   docker run -p 8000:8000 my-agent:latest

3. Serverless（无服务器部署）
   可部署到 AWS Lambda、Google Cloud Functions 等平台。

4. 自定义服务器
   使用 FastAPI 或 Flask，将智能体作为依赖集成。

------------------------------------------------
可观测性（Observability）
------------------------------------------------

设置以下环境变量以启用完整可观测能力：

  export LANGSMITH_TRACING=true
  export LANGSMITH_API_KEY="lsv2_..."

启用后可获得以下能力：
  • 实时追踪（Tracing）
  • 性能指标监控
  • 错误监控与告警
  • 运行结果对比分析
  • 用户反馈收集

============================================
""")