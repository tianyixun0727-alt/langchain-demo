#!/usr/bin/env python3
"""Agent-as-tool Pattern — Hierarchical agent composition"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

# Create sub-agent
translator = create_agent(
    llm=llm,
    tools=[],
    system_prompt="You translate text to French. Output only the translation.",
)

@tool
def translate_to_french(text: str) -> str:
    """使用专门的翻译智能体将英文翻译成法文"""
    result = translator.invoke({
        "messages": [{"role": "user", "content": f"Translate: {text}"}]
    })
    return result["messages"][-1]["content"]

# Main agent uses translation as a tool
agent = create_agent(
    llm=llm,
    tools=[translate_to_french],
    system_prompt="You are a multilingual assistant.",
)

print("=== Agent-as-tool Pattern Demo ===")
print("The translator agent is used as a tool by the main agent.")
result = agent.invoke({
    "messages": [{"role": "user", "content": "Translate 'Hello, how are you?' to French"}]
})
print(f"Result: {result['messages'][-1]['content'][:200]}")
