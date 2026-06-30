#!/usr/bin/env python3
"""Hybrid RAG：查询改写 + 多查询检索 + 重排序（Qdrant 版本）"""

import os
import requests
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

# ---------- 1. 配置 LLM 和嵌入模型 ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

embeddings = OpenAIEmbeddings(
    model="bge-m3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
)

# ---------- 2. 读取知识库 ----------
kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
if not os.path.exists(kb_path):
    raise FileNotFoundError(f"知识库文件不存在: {kb_path}")

texts = []
metadatas = []
with open(kb_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 1)
        if len(parts) == 2:
            doc_id, content = parts
            texts.append(content)
            metadatas.append({"id": doc_id})

print(f"📚 已加载 {len(texts)} 条知识片段")

# ---------- 3. 管理 Qdrant collection ----------
COLLECTION_NAME = "rag_docs_hybrid"
client = QdrantClient(host="localhost", port=6333)
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    print(f"🗑️  已删除旧 collection: {COLLECTION_NAME}")

# ---------- 4. 构建 Qdrant 向量库 ----------
vectorstore = Qdrant.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    collection_name=COLLECTION_NAME,
    distance_func="Cosine",
    location="localhost:6333",
)
print(f"✅ 向量库已就绪（Qdrant, collection: {COLLECTION_NAME}）")

# ---------- 5. 查询改写：生成多个变体 ----------
def expand_query(query: str) -> List[str]:
    """
    使用 LLM 生成 2 个语义相近但表达不同的变体问题。
    返回包含原始查询在内的列表（最多 3 个）。
    """
    prompt = f"""用户原始问题：{query}

请生成 2 个语义相近但表达不同的变体问题，用于从知识库中检索相关信息。
每个变体占一行，只输出问题本身，不要编号或额外说明。

变体问题："""
    response = llm.invoke(prompt)
    variants = [line.strip() for line in response.content.strip().split("\n") if line.strip()]
    # 去重并确保原始查询在首位
    all_queries = [query] + [v for v in variants if v and v != query][:2]
    return all_queries

# ---------- 6. 向量检索（对单个查询，使用 Qdrant 原生过滤） ----------
def retrieve_single(query: str, k: int = 4, threshold: float = 0.5) -> List[dict]:
    """
    使用 Qdrant 检索，返回包含 content 和 score 的文档列表。
    """
    docs_with_score = vectorstore.similarity_search_with_score(
        query=query,
        k=k,
        score_threshold=threshold
    )
    results = []
    for doc, score in docs_with_score:
        results.append({
            "content": doc.page_content,
            "score": score,
            "id": doc.metadata.get("id", "未知")
        })
    return results

# ---------- 7. 重排序（尝试调用 bge-reranker-m3 API，失败则降级） ----------
def rerank_documents(query: str, documents: List[dict], top_k: int = 3) -> List[dict]:
    """
    使用 bge-reranker-m3 重排序（若 API 不可用则按原始分数降序排列）。
    输入：query 和文档列表（每个元素包含 content 和 score）
    输出：重排序后的文档列表（前 top_k 个）
    """
    if not documents:
        return []

    # 准备 API 请求
    payload = {
        "query": query,
        "documents": [doc["content"] for doc in documents],
    }
    headers = {
        "Authorization": f"Bearer NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            "http://10.187.126.181:3000/v1/rerank",
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            raise ValueError("Empty rerank results")

        # 按 relevance_score 降序排列
        sorted_indices = sorted(results, key=lambda x: x.get("relevance_score", 0.0), reverse=True)
        reranked = []
        for item in sorted_indices:
            idx = item["index"]
            if 0 <= idx < len(documents):
                reranked.append(documents[idx])
        return reranked[:top_k]

    except Exception as e:
        print(f"⚠️ 重排序 API 调用失败: {e}，降级为按向量相似度排序。")
        # 降级：按原始分数降序排列
        sorted_docs = sorted(documents, key=lambda x: x["score"], reverse=True)
        return sorted_docs[:top_k]

# ---------- 8. Hybrid RAG 主流程 ----------
def hybrid_rag(query: str) -> str:
    print(f"\n🔍 原始问题: {query}")

    # Step 1: 查询改写
    queries = expand_query(query)
    print(f"📝 扩展查询: {queries}")

    # Step 2: 多查询向量检索（合并去重）
    candidate_docs = []
    for q in queries:
        docs = retrieve_single(q, k=4, threshold=0.4)   # 每个查询取 4 个
        candidate_docs.extend(docs)

    # 去重（按内容去重）
    seen_content = set()
    unique_docs = []
    for doc in candidate_docs:
        if doc["content"] not in seen_content:
            seen_content.add(doc["content"])
            unique_docs.append(doc)

    print(f"📄 候选文档（去重前: {len(candidate_docs)} 条，去重后: {len(unique_docs)} 条）")

    # 展示前几个候选（便于观察）
    print("  候选摘要：")
    for i, doc in enumerate(unique_docs[:3], 1):
        preview = doc["content"][:40].replace('\n', ' ')
        print(f"    [{i}] ID:{doc['id']} (相似度: {doc['score']:.3f}) {preview}...")

    # Step 3: 重排序
    reranked = rerank_documents(query, unique_docs, top_k=3)
    print(f"📊 重排序后取前 {len(reranked)} 个最相关文档：")
    for i, doc in enumerate(reranked, 1):
        print(f"  [{i}] ID:{doc['id']} (相似度: {doc['score']:.3f}) {doc['content'][:40]}...")

    # Step 4: 生成回答
    if reranked:
        context = "\n\n".join([doc["content"] for doc in reranked])
    else:
        context = "（未找到相关文档）"

    system_msg = f"你是一个知识助手，请基于以下参考信息回答用户问题。如果信息不足，请说明。\n\n参考信息：\n{context}"
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": query}
    ]
    response = llm.invoke(messages)
    return response.content

# ---------- 9. 测试 ----------
if __name__ == "__main__":
    print("=== Hybrid RAG 演示（查询改写 + 多查询检索 + 重排序）===")

    # 测试一个典型问题
    query = "苹果是一种常见的水果，味道甜美，富含维生素C"
    answer = hybrid_rag(query)
    print(f"\n🤖 最终回答:\n{answer}")