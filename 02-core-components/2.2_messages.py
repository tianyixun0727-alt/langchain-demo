#!/usr/bin/env python3
"""LangChain Messages 类型示例（tuple写法 + Message类导入）"""

from langchain.chat_models import init_chat_model

# Message类导入（官方标准方式）
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

# 初始化模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="openai",
    api_key="你的_API_KEY",
    base_url="https://api.deepseek.com",
)

# =========================================================
# 1️⃣ System Message（系统消息）
# 作用：控制AI行为和角色设定
# =========================================================
response1 = llm.invoke([
    ("system", "你是一个简洁的助手"),
    ("human", "用一句话解释LangChain")
])

print("\n===== 系统消息示例（tuple） =====\n")
print(response1.content)


# =========================================================
# 2️⃣ Human Message（用户消息）
# 作用：表示用户输入
# =========================================================
response2 = llm.invoke([
    ("human", "什么是LangChain？")
])

print("\n===== 用户消息示例（tuple） =====\n")
print(response2.content)


# =========================================================
# 3️⃣ AI Message（AI消息）
# 作用：模型生成的回复内容
# =========================================================
response3 = llm.invoke([
    ("human", "打个招呼")
])

print("\n===== AI消息示例（tuple） =====\n")
print(response3.content)


# =========================================================
# 4️⃣ Tool Message（工具消息结构演示）
# 作用：表示外部工具返回的结果
# =========================================================
tool_messages_demo = [
    ("human", "纽约天气怎么样？"),
    ("ai", "我需要调用天气工具"),
    ("tool", "纽约天气：25°C，晴天"),
    ("ai", "纽约现在是25°C，天气晴朗")
]

response4 = llm.invoke(tool_messages_demo)

print("\n===== 工具消息示例（tuple结构） =====\n")
print(response4.content)


# =========================================================
# 5️⃣ Message对象写法（对比用）
# =========================================================
messages_obj = [
    SystemMessage(content="你是一个简洁的助手"),
    HumanMessage(content="北京今天天气如何？"),
    AIMessage(content="我正在查询天气信息"),
    ToolMessage(content="北京天气：22°C，多云", tool_call_id="demo")
]

response5 = llm.invoke(messages_obj)

print("\n===== Message对象写法（对比） =====\n")
print(response5.content)