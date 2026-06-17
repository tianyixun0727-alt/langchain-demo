#!/usr/bin/env python3
"""Retrieval Demo 3: Hybrid RAG（查询改写 + 重排序）"""

from langchain_openai import ChatOpenAI

# ---------- 1. 模拟文档库 ----------
DOCUMENTS = [
    {"id": "doc1", "content": "LangChain 是一个用于构建 LLM 应用的框架，支持链式调用、工具集成和智能体。"},
    {"id": "doc2", "content": "RAG（检索增强生成）通过外部知识库检索来增强 LLM 的生成能力，减少幻觉。"},
    {"id": "doc3", "content": "DeepSeek 是深度求索公司开发的大语言模型，支持多种语言和长上下文。"},
    {"id": "doc4", "content": "向量存储（如 Chroma、FAISS）用于存储文本的向量表示，实现语义相似性搜索。"},
    {"id": "doc5", "content": "Agent 是 LangChain 的核心组件之一，可以自主决策调用工具。"},
    {"id": "doc6", "content": "检索增强生成（RAG）是目前减少大模型幻觉的主要技术方案。"},
]

# ---------- 2. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com",
    temperature=0,
)

# ---------- 3. 检索前：查询改写（生成多个查询变体） ----------
def expand_query(query: str) -> list[str]:
    """
    使用 LLM 生成多个相关查询变体，提高召回率。
    """
    prompt = f"""用户原始问题：{query}

请生成 2 个语义相近但表达不同的变体问题，用于检索补充信息。
每个变体一行，只输出问题本身，不要编号。

变体问题："""
    response = llm.invoke(prompt)
    variants = [line.strip() for line in response.content.strip().split("\n") if line.strip()]
    # 去重并保留原始查询
    all_queries = [query] + variants[:2]
    return all_queries

# ---------- 4. 基础检索（关键词匹配） ----------
def basic_retrieve(query: str, top_k: int = 3) -> list[tuple[str, int]]:
    """关键词匹配检索，返回 (文档内容, 匹配分数)"""
    query_words = set(query.lower().split())
    results = []
    for doc in DOCUMENTS:
        doc_words = set(doc["content"].lower().split())
        match_count = len(query_words & doc_words)
        if match_count > 0:
            results.append((doc["content"], match_count))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]

# ---------- 5. 检索后：重排序（LLM 相关性打分） ----------
def rerank(query: str, candidates: list[str]) -> list[str]:
    """
    使用 LLM 对候选文档进行相关性评分并排序。
    返回按相关性降序排列的文档列表。
    """
    if not candidates:
        return []
    
    # 构建打分提示词
    docs_text = "\n\n".join([f"[文档{i+1}] {doc}" for i, doc in enumerate(candidates)])
    prompt = f"""请评估以下文档与用户问题的相关性，按从高到低排序。
只输出文档编号顺序（用逗号分隔），例如：3,1,2

用户问题：{query}

{docs_text}

排序结果："""
    response = llm.invoke(prompt)
    
    # 解析排序结果
    try:
        # 提取数字
        import re
        numbers = re.findall(r'\d+', response.content)
        indices = [int(n) - 1 for n in numbers if 1 <= int(n) <= len(candidates)]
        # 按排序结果重新排列
        sorted_docs = [candidates[i] for i in indices if i < len(candidates)]
        # 补充未出现的文档（放在末尾）
        remaining = [doc for i, doc in enumerate(candidates) if i not in indices]
        return sorted_docs + remaining
    except:
        # 解析失败时返回原顺序
        return candidates

# ---------- 6. Hybrid RAG 完整流程 ----------
def hybrid_rag(query: str) -> str:
    print(f"\n🔍 原始问题: {query}")

    # Step 1: 查询改写（检索前增强）
    queries = expand_query(query)
    print(f"📝 扩展查询: {queries}")

    # Step 2: 多查询检索（合并结果）
    all_candidates = []
    for q in queries:
        results = basic_retrieve(q, top_k=2)
        for doc, score in results:
            all_candidates.append(doc)
    
    # 去重（保留首次出现）
    seen = set()
    unique_candidates = []
    for doc in all_candidates:
        if doc not in seen:
            seen.add(doc)
            unique_candidates.append(doc)
    print(f"📄 候选文档（去重前: {len(all_candidates)} 条，去重后: {len(unique_candidates)} 条）")

    # Step 3: 重排序（检索后增强）
    reranked = rerank(query, unique_candidates)
    print(f"📊 重排序后取前 2 个:")
    for i, doc in enumerate(reranked[:2], 1):
        print(f"  [{i}] {doc[:60]}...")

    # Step 4: 生成回答（取前 2 个最相关文档）
    context = "\n\n".join(reranked[:2]) if reranked else "（未找到相关文档）"
    prompt = f"""基于以下参考信息回答用户问题。如果信息不足，请说明。

参考信息：
{context}

用户问题：{query}

回答："""
    response = llm.invoke(prompt)
    return response.content

# ---------- 7. 测试 ----------
if __name__ == "__main__":
    print("=== Hybrid RAG 演示（查询改写 + 重排序）===")
    
    query = "如何减少大模型幻觉？"
    answer = hybrid_rag(query)
    print(f"\n🤖 最终回答:\n{answer}")