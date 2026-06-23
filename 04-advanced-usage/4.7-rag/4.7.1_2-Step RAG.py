#!/usr/bin/env python3
"""Retrieval Demo 1: 2-Step RAG（固定检索 + 生成）"""

from langchain_openai import ChatOpenAI

# ---------- 1. 模拟文档库 ----------
DOCUMENTS = [
    {"id": "doc1", "content": "LangChain 是一个用于构建 LLM 应用的框架，支持链式调用、工具集成和智能体。"},
    {"id": "doc2", "content": "RAG（检索增强生成）通过外部知识库检索来增强 LLM 的生成能力，减少幻觉。"},
    {"id": "doc3", "content": "DeepSeek 是深度求索公司开发的大语言模型，支持多种语言和长上下文。"},
    {"id": "doc4", "content": "向量存储（如 Chroma、FAISS）用于存储文本的向量表示，实现语义相似性搜索。"},
]

# ---------- 2. 模拟检索器（基于关键词匹配） ----------
def retrieve(query: str, top_k: int = 2) -> list[str]:
    """
    简单的关键词检索：返回包含查询关键词的前 top_k 个文档。
    实际生产环境应替换为向量检索（如 Chroma + 嵌入模型）。
    """
    results = []
    for doc in DOCUMENTS:
        # 检查文档内容是否包含查询中的任何词（简单分词）
        query_words = set(query.lower().split())
        doc_words = set(doc["content"].lower().split())
        # 计算匹配词数
        match_count = len(query_words & doc_words)
        if match_count > 0:
            results.append((doc["content"], match_count))
    # 按匹配词数降序排序，取前 top_k
    results.sort(key=lambda x: x[1], reverse=True)
    return [content for content, _ in results[:top_k]]

# ---------- 3. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

# ---------- 4. 2-Step RAG 流程 ----------
def rag_pipeline(user_query: str) -> str:
    # Step 1: 检索
    docs = retrieve(user_query)
    context = "\n\n".join(docs)
    print(f"📄 检索到 {len(docs)} 个相关文档片段：")
    for i, doc in enumerate(docs, 1):
        print(f"  [{i}] {doc[:60]}...")
    print()

    # Step 2: 生成（基于检索结果构建提示词）
    prompt = f"""基于以下参考信息回答用户问题。如果信息不足，请直接说明。

参考信息：
{context if context else "（未找到相关文档）"}

用户问题：{user_query}

回答："""
    response = llm.invoke(prompt)
    return response.content

# ---------- 5. 测试 ----------
if __name__ == "__main__":
    query = "什么是 RAG？"
    print(f"❓ 用户提问: {query}\n")
    answer = rag_pipeline(query)
    print(f"🤖 最终回答:\n{answer}")