#!/usr/bin/env python3
"""Multi-agent Systems — Overview of All 5 Patterns"""

print("""
============================================
Multi-agent Systems — Overview
============================================

Multi-agent systems coordinate specialized components to tackle complex
workflows. However, not every complex task requires this approach — a
single agent with the right tools and prompt can often achieve similar
results.

为什么需要多智能体？
----------------
  • Context Management: Provide specialized knowledge without
    overwhelming the model's context window.
  • Distributed Development: Different teams develop and maintain
    capabilities independently.
  • Parallelization: Spawn specialized workers for subtasks and
    execute them concurrently.

For built-in multi-agent support, use Deep Agents — a higher-level
harness built on LangChain with subagents, skills, planning, a
virtual filesystem, and context management.

The 5 Patterns
--------------

Pattern        | How It Works                          | Best For
---------------|---------------------------------------|--------------------------
1. Subagents   | Main agent coordinates subagents      | Distributed development,
               | as tools. All routing passes through  | parallel execution,
               | the main agent.                       | multi-hop reasoning
               |                                       |
2. Handoffs    | Behavior changes dynamically via      | Sequential specialized
               | tool calls updating state. Agents     | processing, direct user
               | transfer control to each other.       | interaction
               |                                       |
3. Skills      | Specialized prompts and knowledge     | Single-agent stays in
               | loaded on-demand. A single agent      | control, context
               | stays in control.                     | management
               |                                       |
4. Router      | A routing step classifies input and   | Input classification,
               | directs to specialized agents.        | dispatch patterns
               | Results are synthesized.              |
               |                                       |
5. Custom      | Build bespoke execution flows with   | Complex deterministic +
Workflow       | LangGraph. Mix deterministic logic   | agentic workflows
               | and agentic behavior.                |

Run the individual pattern demos:
  python 02_subagents.py
  python 03_handoffs.py
  python 04_skills.py
  python 05_router.py
  python 06_custom_workflow.py
""")
