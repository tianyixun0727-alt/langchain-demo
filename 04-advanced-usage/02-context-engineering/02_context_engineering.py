#!/usr/bin/env python3
"""上下文工程 — 动态提示词"""

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt
from langchain.agents.runtime import ModelRequest
from langchain_openai import ChatOpenAI


@dynamic_prompt
def smart_prompt(request: ModelRequest) -> ModelRequest:
    """根据对话长度动态调整系统提示词"""
    n = len(request.state.get("messages", []))
    if n > 10:
        request.system_prompt = "The conversation is long. Be concise."
    else:
        request.system_prompt = "You are a helpful assistant."
    return request

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

agent = create_agent(
    llm=llm,
    middleware=[smart_prompt],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Tell me about context engineering."}]
})
print(f"Context engineering demo:")
print(result['messages'][-1]['content'][:200])
