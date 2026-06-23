#!/usr/bin/env python3
"""模型初始化与调用"""

from langchain.chat_models import init_chat_model
#这一行导入的是 LangChain 的统一模型初始化方法
#用统一方式初始化不同厂商的 LLM（OpenAI / DeepSeek / Anthropic）

# 初始化 DeepSeek 模型（兼容 OpenAI API）
llm = init_chat_model(
    model="deepseek-v3",
    model_provider="openai",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
)

print("Model: DeepSeek Chat (via OpenAI compatible API)")

# 简单的模型调用
response = llm.invoke([
    {"role": "user", "content": "Say 'Hello, LangChain!' in 3 words"}
])
print(f"Response: {response.content}")
#让模型用 3 个词说 Hello LangChain 
#模型会：理解输入,生成回答,返回结果

# 构造多轮对话上下文
messages = [
    {"role": "system", "content": "You speak like a pirate."},
    {"role": "user", "content": "Introduce yourself."},
]

reply = llm.invoke(messages)
print(f"Pirate: {reply.content}")

# invoke vs stream
# invoke(): 一次性返回完整结果（等待全部生成完）
# stream(): 流式返回，边生成边输出（适合实时显示）