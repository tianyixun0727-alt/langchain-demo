#!/usr/bin/env python3
"""预置中间件示例：自动摘要（SummarizationMiddleware）

功能：当对话累积到一定长度时，自动将早期消息压缩为摘要，
      防止上下文超长（token 溢出）。
"""

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_openai import ChatOpenAI

# ----- 1. 初始化 LLM -----
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

# ----- 2. 创建摘要中间件 -----
summarizer = SummarizationMiddleware(
    model=llm,
    max_tokens=100,      # 摘要最大 token 数（适当调大，保留更多关键信息）
    keep_last=5,         # 保留最近 5 条原始消息（避免最新信息被压缩）
)

# ----- 3. 创建 Agent（带中间件） -----
agent = create_agent(
    model=llm,
    tools=[],               # 无工具，仅演示摘要功能
    middleware=[summarizer],
    system_prompt="你是一个友好的助手，请基于对话历史回答问题。",
)

# ----- 4. 模拟一段长对话 -----
long_chat = [
    "我叫小明，住在北京朝阳区。",
    "我喜欢打篮球和游泳，周末经常去健身房。",
    "我是一名软件工程师，工作五年了。",
    "我家里养了一只金毛犬，名字叫旺财。",
    "上个月我去了一趟云南旅游，大理和丽江都去了。",   # 注意逗号
    "我之前问过什么？"
]

# ----- 5. 循环调用 Agent，维护完整历史 -----
history = []   # 存储全部消息（用户 + 助手）
for user_msg in long_chat:
    # 1) 添加用户消息到历史
    history.append({"role": "user", "content": user_msg})
    
    # 2) 调用 Agent，传入完整历史
    result = agent.invoke({"messages": history})
    
    # 3) 提取助手回复并添加到历史
    assistant_reply = result["messages"][-1].content
    history.append({"role": "assistant", "content": assistant_reply})
    
    # 4) 打印当前轮次
    print(f"用户: {user_msg}")
    print(f"助手: {assistant_reply}\n")

# ----- 6. 观察效果 -----
print("=" * 50)
print("此时 history 包含所有用户消息和助手回复。")
print(f"总消息数: {len(history)} 条")
print("由于 SummarizationMiddleware 会在上下文接近阈值时自动压缩，")
print("因此即使对话很长，也能保持 token 在限制以内。")