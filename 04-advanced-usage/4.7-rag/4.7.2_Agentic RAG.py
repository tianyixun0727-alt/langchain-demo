#!/usr/bin/env python3
"""Retrieval Demo 2: Agentic RAG（Agent 自主决策检索）"""
#将检索能力包装成工具 search_knowledge_base，交给 LangChain Agent，由 LLM 自主判断是否需要检索
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# ---------- 1. 模拟文档库 ----------
DOCUMENTS = [
    {"id": "doc1", "content": "LangChain 是一个用于构建 LLM 应用的框架，支持链式调用、工具集成和智能体。"},
    {"id": "doc2", "content": "RAG（检索增强生成）通过外部知识库检索来增强 LLM 的生成能力，减少幻觉。"},
    {"id": "doc3", "content": "DeepSeek 是深度求索公司开发的大语言模型，支持多种语言和长上下文。"},
    {"id": "doc4", "content": "向量存储（如 Chroma、FAISS）用于存储文本的向量表示，实现语义相似性搜索。"},
]

# ---------- 2. 检索工具（Agent 的工具箱） ----------
@tool
def search_knowledge_base(query: str) -> str:
    """
    在知识库中搜索与查询相关的内容。
    当用户询问关于 LangChain、RAG、DeepSeek、向量存储等主题时使用。
    """
    query_words = set(query.lower().split())
    results = []
    for doc in DOCUMENTS:
        doc_words = set(doc["content"].lower().split())
        match_count = len(query_words & doc_words)
        if match_count > 0:
            results.append((doc["content"], match_count))
    
    if not results:
        return "知识库中未找到相关信息。"
    
    results.sort(key=lambda x: x[1], reverse=True)
    # 返回前 2 个最相关的文档
    return "\n\n".join([content for content, _ in results[:2]])

# ---------- 3. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

# ---------- 4. 创建 Agent（注入检索工具） ----------
agent = create_agent(
    model=llm,
    tools=[search_knowledge_base],
    system_prompt="""你是一个知识助手。
    
    规则：
    1. 当用户询问知识库相关问题（如 LangChain、RAG、DeepSeek、向量存储）时，必须使用 search_knowledge_base 工具检索。
    2. 如果用户问的是常识问题（如天气、数学），可以直接回答，无需检索。
    3. 基于检索结果回答，并引用来源。
    """
)

# ---------- 5. 测试（Agent 自主决策） ----------
def ask(question: str):
    print(f"\n❓ 用户: {question}")
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    print(f"🤖 助手: {result['messages'][-1].content}")

if __name__ == "__main__":
    print("=== Agentic RAG 演示（Agent 自主决定是否检索）===")
    
    # 场景1：需要检索（知识库问题）
    ask("什么是 RAG？")
    
    # 场景2：需要检索（知识库问题）
    ask("LangChain 是什么？")
    
    # 场景3：不需要检索（常识问题）
    ask("1 + 1 等于几？")
    
    # 场景4：需要检索（知识库问题）
    ask("DeepSeek 是什么模型？")