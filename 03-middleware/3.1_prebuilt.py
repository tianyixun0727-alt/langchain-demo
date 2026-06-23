#中间件（Middleware）的作用是在不修改 Agent 核心代码的情况下
# 在 Agent 执行流程的某些阶段插入额外逻辑，对模型调用过程进行增强和控制。
# !/usr/bin/env python3
"""预置中间件示例：自动摘要（SummarizationMiddleware）"""
#当对话越来越长，LLM 上下文会爆掉（token 超限）,自动把“长对话压缩成摘要”，避免上下文无限增长
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

summarizer = SummarizationMiddleware(
    model=llm,
    max_tokens=400,# 摘要的最大 token 数
    keep_last=200  # 保留最近的消息数，避免丢失重要上下文
)

agent = create_agent(
    model=llm,
    tools=[],
    middleware=[summarizer],
)

# 模拟一段长对话
long_chat = [
    "我叫小明，住在北京朝阳区。",
    "我喜欢打篮球和游泳，周末经常去健身房。",
    "我是一名软件工程师，工作五年了。",
    "我家里养了一只金毛犬，名字叫旺财。",
    "上个月我去了一趟云南旅游，大理和丽江都去了。",
]

for msg in long_chat:#循环调用 Agent
    result = agent.invoke({
        "messages": [{"role": "user", "content": msg}]
    })

    print(f"用户: {msg}")
    print(f"助手: {result['messages'][-1]['content'][:100]}\n")