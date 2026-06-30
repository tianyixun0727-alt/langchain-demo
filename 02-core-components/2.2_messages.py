#!/usr/bin/env python3
"""LangChain Messages 完整演示"""

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

# ---------- 初始化模型（使用你的配置） ----------
llm = init_chat_model(
    model="deepseek-v3",
    model_provider="openai",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
)

print("=" * 60)
print("LangChain Messages 官方文档示例")
print("=" * 60)

# ============================================================
# 1️⃣ SystemMessage + HumanMessage（元组简写）
# ============================================================
print("\n【示例 1】System + Human（元组写法）")
response1 = llm.invoke([
    ("system", "你是一位简洁的编程助手。"),
    ("human", "Python 中如何用列表推导式生成平方数？")
])
print("回复：", response1.content, "\n")

# ============================================================
# 2️⃣ 多轮对话（对象写法，含模拟历史）
# ============================================================
print("\n【示例 2】多轮对话（对象写法）")
messages_2 = [
    SystemMessage(content="你是一位友好的导游。"),
    HumanMessage(content="我想去北京旅游。"),
    AIMessage(content="太好了！北京有很多名胜古迹。"),
    HumanMessage(content="请推荐三个必去景点。")
]
response2 = llm.invoke(messages_2)
print("回复：", response2.content, "\n")

# ============================================================
# 3️⃣ 工具调用流程（AIMessage + tool_calls → ToolMessage → 模型回复）
# ============================================================
print("\n【示例 3】工具调用（含 tool_calls 和 ToolMessage）")

# 模拟：模型请求调用 get_weather 工具
# 注意：AIMessage 必须包含 tool_calls，且每个调用有唯一 id
tool_conversation = [
    HumanMessage(content="纽约今天的天气怎么样？"),
    AIMessage(
        content="我需要调用天气工具来获取数据。",
        tool_calls=[#模型决定调用哪个工具，以及调用参数是什么
            {
                "id": "weather_001",
                "name": "get_weather",
                "args": {"city": "New York"}
            }
        ]
    ),
    ToolMessage(
        content="纽约天气：晴天，25°C，湿度 60%",
        tool_call_id="weather_001"   # 必须与上方的 id 匹配
    )
    # 注意：这里不要再手动添加 AIMessage，模型会基于 ToolMessage 自动生成最终回复
]

response3 = llm.invoke(tool_conversation)
print("模型基于工具结果生成的回复：", response3.content, "\n")
