#!/usr/bin/env python3
"""预置中间件示例：PII 检测"""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_openai import ChatOpenAI


# 创建带 PII 检测的智能体
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
        PIIMiddleware("credit_card", strategy="block", apply_to_input=True),
    ],
)

# 测试 PII 脱敏效果
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "My email is john@example.com and my card is 4111-1111-1111-1111."
    }]
})
print(f"Input contained PII, middleware handled it.")
print(f"Response: {result['messages'][-1]['content'][:100]}...")
