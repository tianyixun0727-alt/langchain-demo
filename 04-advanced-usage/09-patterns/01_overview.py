#!/usr/bin/env python3
"""Agent Development Patterns — Complete Overview"""

print("""
============================================
Agent Development Patterns — Complete Guide
============================================

1. 单智能体模式
   一个模型 + one set of tools + one loop.
   The simplest pattern. Start here for most use cases.
   ---
   from langchain.agents import create_agent
   agent = create_agent(llm=llm, tools=[...])

2. 深度智能体
   Batteries-included with automatic context compression,
   virtual filesystem, planning, and sub-agent spawning.
   ---
   from deepagents import create_deep_agent
   agent = create_deep_agent(llm=llm, tools=[...])

3. 多智能体编排
   See 06-multi-agent/ for all 5 patterns:
   • Subagents — Main agent coordinates specialized sub-agents
   • Handoffs — Agents transfer control dynamically
   • Skills — Single agent loads knowledge on demand
   • Router — Classify and dispatch to specialized agents
   • Custom Workflow — LangGraph for bespoke flows

4. 人机协作
   Pause for human approval on sensitive operations.
   ---
   middleware=[HumanInTheLoopMiddleware(interrupt_on={...})]

5. 智能体即工具
   Agents can be used as tools within other agents,
   enabling hierarchical composition.
   ---
   @tool
   def sub_agent_task(task: str) -> str:
       sub = create_agent(llm=llm, tools=[...])
       return sub.invoke(...)

6. 流式优先
   Build agents with streaming for responsive UIs.
   ---
   for event in agent.astream_events({...}, version="v2"):
       print(event["event"])

决策指南
--------------
  • Start with 单智能体模式 for most use cases
  • Add Middleware as complexity grows
  • Use 深度智能体 when you need built-in features
  • Use Multi-agent when tasks need specialized components
  • Add HITL for operations requiring human oversight
  • Use 流式优先 for responsive user interfaces
""")
