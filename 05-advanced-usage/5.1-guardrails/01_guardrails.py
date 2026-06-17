#!/usr/bin/env python3
"""Guardrails Demo: PII 脱敏"""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
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