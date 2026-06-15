#!/usr/bin/env python3
"""LangChain vs LangGraph vs MCP — 一个可运行的对比 Demo"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

print("""
============================================
LangChain vs LangGraph vs MCP
一个可运行的对比 Demo
============================================

这三个技术协同工作:
  • LangChain = 智能体框架 (high-level)
  • LangGraph = 编排框架 (low-level)
  • MCP = 工具和数据协议 (shared tools)

演示：展示每一层的简单智能体.
""")

# === LangChain Layer ===
print("=== 1. LangChain Layer (Agent Harness) ===")
print("create_agent gives us the harness: model + tools + middleware\n")

@tool
def calculator(expression: str) -> str:
    """计算数学表达式的结果"""
    try:
        return str(eval(expression))
    except:
        return "Error evaluating expression"

agent = create_agent(
    llm=llm,
    tools=[calculator],
    system_prompt="You are a math assistant. Use the calculator tool.",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 2 + 3 * 4?"}]
})
print(f"Agent result: {result['messages'][-1]['content'][:100]}")
print()

# === LangGraph Layer ===
print("=== 2. LangGraph Layer (Orchestration) ===")
print("LangChain agents run on LangGraph's runtime under the hood.")
print("LangGraph provides: checkpointing, persistence, human-in-the-loop\n")
print("  from langgraph.graph import StateGraph")
print("  graph = StateGraph(AgentState)")
print("  graph.add_node('agent', agent_node)")
print("  graph.add_edge(START, 'agent')")
print("  chain = graph.compile()")
print()

# === MCP Layer ===
print("=== 3. MCP Layer (Protocol) ===")
print("MCP connects models with external tools via a standard protocol.")
print("LangChain agents can use MCP tools like any other tool.\n")
print("  from langchain.mcp import MCPTool")
print("  mcp_tools = MCPTool.from_server('http://localhost:8000/mcp')")
print("  agent = create_agent(llm=llm, tools=[*mcp_tools, local_tool])")
print()

# 总结
print("=" * 44)
print("总结")
print("=" * 44)
table = """
Dimension        | LangChain        | LangGraph            | MCP
-----------------|------------------|----------------------|---------------------
抽象层级      | High (agents)    | Low (state graphs)   | 协议层
核心 API      | create_agent()   | StateGraph, add_node | MCPTool.from_server()
状态管理 | Built-in         | Explicit state graph | 不适用
多智能体      | Built-in patterns| Custom orchestration | 工具共享
使用场景         | 快速构建智能体     | 复杂控制流 | 跨应用工具
"""
print(table)
print("See docs/comparison.md for full details.")
