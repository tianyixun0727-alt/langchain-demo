#!/usr/bin/env python3
"""Deploy Demo：将 LangChain Agent 部署成 HTTP 服务"""
#安装依赖:pip install fastapi uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import uvicorn


# =========================================================
# 1️⃣ 定义工具
# =========================================================

@tool
def get_weather(city: str) -> str:
    """查询天气"""
    return f"{city} 今天晴天，25°C。"


# =========================================================
# 2️⃣ 创建 Agent
# =========================================================

llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="你的API_KEY",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="你是一个天气助手。"
)


# =========================================================
# 3️⃣ 创建 Web 服务
# =========================================================

app = FastAPI(
    title="LangChain Deploy Demo"
)


# 请求格式
class ChatRequest(BaseModel):
    message: str


# =========================================================
# 4️⃣ 定义 API 接口
# =========================================================

@app.post("/chat")
def chat(req: ChatRequest):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": req.message
                }
            ]
        }
    )

    return {
        "answer": result["messages"][-1].content
    }


# =========================================================
# 5️⃣ 启动服务
# =========================================================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )