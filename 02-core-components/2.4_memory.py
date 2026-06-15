#!/usr/bin/env python3
"""短期记忆：智能体记住对话上下文"""

from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


checkpointer = InMemorySaver()
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

agent = create_agent(
    llm=llm,
    tools=[],
    checkpointer=checkpointer,
)

# 第一轮
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Alice."}]},
    config={"configurable": {"thread_id": "thread-1"}},
)
print("Round 1: Told the agent my name.")

# 第二轮 — 智能体记住了
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my name?"}]},
    config={"configurable": {"thread_id": "thread-1"}},
)
print(f"Round 2: {result['messages'][-1]['content']}")
