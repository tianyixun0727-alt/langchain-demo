#!/usr/bin/env python3
"""上下文工程 Demo 1: 模型上下文 - 动态系统提示词"""

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt #引入动态提示词中间件
from langchain.agents.middleware.types import ModelRequest 
from langchain_openai import ChatOpenAI


# ---------- 1. 定义动态提示词 ----------
@dynamic_prompt
def length_aware_prompt(request: ModelRequest) -> str:
    """
    根据当前对话消息数量，返回不同的系统提示词。
    这个函数会在每次模型调用前被执行，返回值会作为 system prompt。
    """
    message_count = len(request.messages)  # 当前对话已有消息数
    
    base = "你是一个乐于助人的助手。"
    
    if message_count > 10:
        # 长对话：要求简洁回复
        base += " 当前对话较长，请用最简洁的语言回答问题，不要赘述。"
    elif message_count > 5:
        # 中等对话：可以详细一些
        base += " 请给出清晰、有条理的回复。"
    else:
        # 短对话：正常回复
        base += " 请友好地回答问题。"
    
    return base


# ---------- 2. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com",
    temperature=0,
)


# ---------- 3. 创建 Agent（注入动态提示词中间件） ----------
agent = create_agent(
    model=llm,
    tools=[],  # 本例无工具
    middleware=[length_aware_prompt],  # 动态提示词作为中间件
)


# ---------- 4. 测试 ----------
# 模拟短对话（只有1条用户消息）
result1 = agent.invoke({
    "messages": [{"role": "user", "content": "介绍一下你自己"}]
})
print("短对话回复（应该较详细）：")
print(result1["messages"][-1].content)
print("\n" + "-"*50 + "\n")

# 模拟长对话：先发送多条消息填充历史
messages = []
for i in range(1, 13):  # 先发12条用户消息，使消息数 > 10
    messages.append({"role": "user", "content": f"这是第{i}条消息"})
    agent.invoke({"messages": messages})  # 逐步构建上下文

# 最后再问一个问题
messages.append({"role": "user", "content": "现在请简洁回答：1+1=?"})
result2 = agent.invoke({"messages": messages})
print("长对话回复（应该很简洁）：")
print(result2["messages"][-1].content)