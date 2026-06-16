#!/usr/bin/env python3
"""安全机制 — Guardrails 与 PII 检测"""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

agent = create_agent(
    llm=llm,
    tools=[],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
    ],
)

sensitive_input = "Contact me at alice@company.com or call 555-1234."
result = agent.invoke({
    "messages": [{"role": "user", "content": sensitive_input}]
})
print(f"Original input contained: alice@company.com")
print(f"PII was auto-redacted before reaching the model.")
print(f"Response: {result['messages'][-1]['content'][:150]}")
