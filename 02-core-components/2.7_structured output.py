#!/usr/bin/env python3
"""创建智能体并获取结构化输出"""
# 让 LLM 输出"可解析的结构化结果"，而不是纯文本

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import json, re


class Answer(BaseModel):
    summary: str = Field(description="Brief summary")
    confidence: float = Field(ge=0, le=1, description="Confidence score")


llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
)


# ========== 方式1: Agent + prompt 引导 JSON 输出 ==========
# 通过 system_prompt 引导模型输出 JSON，再手动解析为 Pydantic 对象
# 兼容性最好，适用于所有模型
print("=" * 50)
print("方式1: Agent + prompt 引导 JSON 输出")
print("=" * 50)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=(
        "You are a research assistant. Be concise. "
        "You MUST respond ONLY with a JSON object containing exactly two keys: "
        "'summary' (string) and 'confidence' (float between 0 and 1). "
        "Do not include any other text outside the JSON object."
    ),
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What are the latest AI trends?"}]
})

raw_content = result["messages"][-1].content
# 提取 JSON 部分（兼容模型可能在 JSON 前后添加文本的情况）
match = re.search(r'\{[^{}]*\}', raw_content, re.DOTALL)
if match:
    parsed = Answer.model_validate_json(match.group())
else:
    parsed = Answer.model_validate_json(raw_content)

print(f"Type: {type(parsed)}")
print(f"Summary: {parsed.summary}")
print(f"Confidence: {parsed.confidence}")
print()