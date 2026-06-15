# 12. 前端支持 — Frontend Overview & Agent Chat UI

## 概述

LangChain 为智能体应用提供丰富的前端 SDK 和 UI 组件。

## 文件说明

| File | Description |
|------|-------------|
| `01_overview.py` | 前端支持概览与 Agent Chat UI |

## 核心能力

| 能力 | 说明 |
|------|------|
| 持久化线程 | 刷新页面、切换设备、重新加入运行而不丢失对话状态 |
| 类型化状态 | 渲染任意状态键（不仅仅是消息） |
| 工具调用生命周期 | 显示待定/完成/失败的工具调用 |
| 中断处理 | 暂停执行等待人工审批，然后继续 |
| 检查点 | 编辑、重试、分支、时间旅行调试 |
| 嵌套执行可视化 | 深度智能体、子智能体可视化 |
| 框架原生响应式 | React / Vue / Svelte / Angular 原生集成 |

## 框架支持

- React: `npm install @langchain/react`
- Vue: `npm install @langchain/vue`
- Svelte: `npm install @langchain/svelte`
- Angular: `npm install @langchain/angular`
