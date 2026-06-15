#!/usr/bin/env python3
"""前端支持与 Agent Chat UI"""

print("""
============================================
前端支持 — Frontend Overview
============================================

LangChain 提供前端 SDK，让你可以为智能体构建
丰富的交互式界面。

架构:
  后端: create_agent() -> 编译的 LangGraph 图 -> stream API
  前端: useStream() / injectStream() -> 响应式状态

支持的框架:
  * React (@langchain/react)
  * Vue (@langchain/vue)
  * Svelte (@langchain/svelte)
  * Angular (@langchain/angular)

核心 UI 原语:
  * useStream() — 连接后端流，获取响应式状态
  * 消息渲染 — 文本、工具调用、推理内容
  * 中断处理 — 暂停/继续执行
  * 状态复现 — 时间旅行调试
  * 自定义状态键渲染 — 不仅仅是消息

Agent Chat UI:
  Agent Chat UI 是一个开源的 Next.js 应用，
  提供与任何 LangChain 智能体交互的对话界面。

  快速开始:
    1. 访问 https://chat.langchain.com
    2. 输入你的部署 URL 或本地地址
    3. 开始对话 — UI 自动渲染工具调用和中断

  本地开发:
    npx create-agent-chat-app --project-name my-chat-ui
    cd my-chat-ui
    pnpm install
    pnpm dev

  连接配置:
    * Graph ID: langgraph.json 中的图名
    * Deployment URL: http://localhost:2024 (本地)
    * LangSmith API Key: (可选，用于远程部署)

使用场景:
  * 智能体聊天界面
  * 人机协作（审批、编辑）
  * 多智能体监控面板
  * 调试和评估工具
============================================
""")

if __name__ == "__main__":
    pass
