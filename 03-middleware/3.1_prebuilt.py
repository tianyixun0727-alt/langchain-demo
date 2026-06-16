#!/usr/bin/env python3
"""预置中间件示例：自动摘要（SummarizationMiddleware）"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

# ✅ 修复后的 middleware（新版 API）
summarizer = SummarizationMiddleware(
    model=llm,
    max_tokens=400,        # 替代 trigger=("tokens", 400)
    keep_last=200          # 替代 keep=200
)

agent = create_agent(
    llm=llm,
    tools=[],
    middleware=[
        summarizer
    ],
)

# 模拟一段长对话
long_chat = [
    "我叫小明，住在北京朝阳区。",
    "我喜欢打篮球和游泳，周末经常去健身房。",
    "我是一名软件工程师，工作五年了。",
    "我家里养了一只金毛犬，名字叫旺财。",
    "上个月我去了一趟云南旅游，大理和丽江都去了。",
]

for msg in long_chat:
    result = agent.invoke({
        "messages": [{"role": "user", "content": msg}]
    })

    print(f"用户: {msg}")
    print(f"助手: {result['messages'][-1]['content'][:100]}\n")