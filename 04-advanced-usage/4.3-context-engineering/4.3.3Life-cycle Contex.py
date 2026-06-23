#!/usr/bin/env python3
"""上下文工程 Demo 3: 生命周期上下文 - 自动摘要"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_openai import ChatOpenAI


# ---------- 1. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)


# ---------- 2. 创建 Agent（带摘要中间件） ----------
agent = create_agent(
    model=llm,
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model=llm,                    # 用于生成摘要的模型
            trigger=("tokens", 300),      # 当 token 超过 300 时触发摘要
            keep=("messages", 5),         # 摘要后保留最近 5 条消息
        )
    ],
)


# ---------- 3. 模拟长对话 ----------
# 逐步发送消息，累积到触发摘要的条件
conversation = []

for i in range(1, 8):
    user_msg = f"这是第{i}条消息，请用一两句话回复我。"
    conversation.append({"role": "user", "content": user_msg})
    
    result = agent.invoke({"messages": conversation})
    assistant_reply = result["messages"][-1].content
    conversation.append({"role": "assistant", "content": assistant_reply})
    
    print(f"第{i}轮: 用户 -> {user_msg}")
    print(f"     助手 -> {assistant_reply[:30]}...")
    print(f"     当前消息数: {len(conversation)}\n")


# ---------- 4. 查看最终状态 ----------
print("=== 最终对话状态 ===")
print(f"总消息数: {len(conversation)}")
# 摘要中间件会将历史消息压缩，但用户可见的是最后几条消息。
# 在长对话中，助手会基于摘要+最近消息来回复。