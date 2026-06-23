#!/usr/bin/env python3
"""Guardrails Demo: PII 脱敏"""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware#引入一个“隐私过滤中间件”
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

agent = create_agent(
    model=llm,
    tools=[],
    middleware=[PIIMiddleware("email", strategy="redact", apply_to_input=True)]
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "My email is john@example.com"}]
})
print(result["messages"][-1].content)