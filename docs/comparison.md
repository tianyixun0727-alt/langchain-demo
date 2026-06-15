# LangChain vs LangGraph vs MCP 对比

| 维度 | LangChain | LangGraph | MCP |
|------|-----------|-----------|-----|
| **定位** | 智能体框架 & SDK | 底层编排框架 | 工具与数据协议 |
| **抽象层级** | 高 — create_agent、中间件 | 低 — StateGraph、节点、边 | 协议 — 工具发现/调用 |
| **核心 API** | create_agent(), @tool, middleware | StateGraph, add_node, add_edge | MCP server, MCPTool.from_server() |
| **状态管理** | 内置通过检查点 | 显式状态图 | 不适用 |
| **循环控制** | 自动智能体循环 | 自定义控制流 | 不适用 |
| **多智能体** | 内置模式 | 自定义编排 | 协议级工具共享 |
| **适用场景** | 大多数智能体应用、快速启动 | 自定义控制流、复杂图 | 跨应用工具/知识共享 |
| **示例** | 问答机器人、研究智能体 | 复杂工作流、流水线 | 连接文档到 AI 助手 |
| **学习曲线** | 低到中 | 中到高 | 中 |
| **集成关系** | 基于 LangGraph | 可将 LangChain 智能体作为节点 | LangChain 和 LangGraph 均可使用 |

## 决策指南

1. **大多数场景** → 从 **LangChain** 开始，这是最快的上手路径
2. **需要自定义控制流** → 使用 **LangGraph** 构建复杂状态图
3. **需要共享工具** → 使用 **MCP** 跨应用连接工具和数据源
4. **三者可无缝协同** → LangChain 智能体运行在 LangGraph 上，两者都可使用 MCP 工具
