#!/usr/bin/env python3
"""创建智能体并获取结构化输出"""
#让 LLM 输出“可解析的结构化结果”，而不是纯文本
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel, Field# Pydantic = 数据模型定义工具  定义结构化输出格式
from langchain_openai import ChatOpenAI


class Answer(BaseModel):
    summary: str = Field(description="Brief summary")
    confidence: float = Field(ge=0, le=1, description="Confidence score")

@tool
def search_web(query: str) -> str:
    """搜索网页获取信息"""
    return f"Simulated results for: {query}"

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

agent = create_agent(
    model=llm,
    tools=[search_web],
    system_prompt="You are a research assistant. Be concise.",
    response_format=Answer,
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What are the latest AI trends?"}]
})

parsed = result["structured_response"]
print(f"Summary: {parsed.summary}")
print(f"Confidence: {parsed.confidence}")
