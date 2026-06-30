#!/usr/bin/env python3
"""短期记忆：智能体记住对话上下文"""

from langgraph.checkpoint.memory import InMemorySaver
#导入记忆组件,保存每个对话线程的状态,每次调用的时候，都可以把之前的消息重新加载回来
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


checkpointer = InMemorySaver()#创建了一个内存存储器,messages 会被保存在内存中,适合演示和测试,如果要长期保存,可以换成数据库存储器
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

agent = create_agent(
    model=llm,
    tools=[],
    checkpointer=checkpointer,
)

# 第一轮
agent.invoke(
    {"messages": [{"role": "user", "content": "My name is Alice."}]},
    config={"configurable": {"thread_id": "thread-1"}},#会话id
)
print("Round 1: Told the agent my name.")

# 第二轮 — 智能体记住了
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my name?"}]},
    config={"configurable": {"thread_id": "thread-1"}},
)
print(f"Round 2: {result['messages'][-1].content}")
