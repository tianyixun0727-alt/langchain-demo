#!/usr/bin/env python3
"""Agentic RAG：Agent 自主决策检索（使用 create_agent + @tool + Qdrant）"""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain.agents import create_agent
from langchain.tools import tool

# ---------- 1. 配置 LLM ----------
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
    temperature=0,
)

# ---------- 2. 配置嵌入模型 ----------
embeddings = OpenAIEmbeddings(
    model="bge-m3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1",
)

# ---------- 3. 从 knowledge_base.txt 加载数据 ----------
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

# ---------- 4. 删除已有 collection（若有） ----------
COLLECTION_NAME = "rag_docs_agentic"
client = QdrantClient(host="localhost", port=6333)
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    print(f"🗑️  已删除旧 collection: {COLLECTION_NAME}")

# ---------- 5. 构建 Qdrant 向量库 ----------
vectorstore = Qdrant.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    collection_name=COLLECTION_NAME,
    distance_func="Cosine",
    location="localhost:6333",
)
print(f"✅ 向量库已就绪（Qdrant, collection: {COLLECTION_NAME}）")

# ---------- 6. 定义检索工具（Agent 的工具箱） ----------
@tool
def search_knowledge_base(query: str) -> str:
    """
    在知识库中搜索与查询相关的内容。
    当用户询问关于水果、动物、编程语言、地理、常识等知识时使用。
    输入为查询字符串，返回最相关的文档内容（最多3条）。
    """
    # 使用 Qdrant 的原生 score_threshold 过滤
    docs_with_score = vectorstore.similarity_search_with_score(
        query=query,
        k=5,
        score_threshold=0.5   # 与两步法保持一致
    )
    if not docs_with_score:
        return "知识库中未找到相关信息。"

    # 打印检索到的片段（便于观察）
    print(f"\n🔍 检索结果（查询：{query}）：")
    for idx, (doc, score) in enumerate(docs_with_score[:3], 1):
        doc_id = doc.metadata.get('id', '未知ID')
        preview = doc.page_content[:40].replace('\n', ' ')
        print(f"  [{idx}] ID:{doc_id} (相似度: {score:.3f}) - {preview}...")

    # 返回文本内容（供LLM阅读）
    results = [f"- {doc.page_content}" for doc, _ in docs_with_score[:3]]
    return "\n".join(results)

# ---------- 7. 创建 Agent ----------
agent = create_agent(
    model=llm,
    tools=[search_knowledge_base],
    system_prompt="""你是一个知识助手，可以访问知识库。

规则：
1. 当用户询问知识库相关问题时，**必须**使用 search_knowledge_base 工具检索信息。
2. 如果用户问的是常识问题（如数学计算、日期等）或不涉及知识库内容，可以直接回答。
3. 基于检索结果回答时，请简要概括关键信息，并保持回答清晰准确。
4. 如果检索结果不足以回答问题，请如实说明。
"""
)

# ---------- 8. 辅助函数：提问并打印结果 ----------
def ask(question: str):
    print(f"\n❓ 用户: {question}")
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    assistant_msg = result["messages"][-1]
    print(f"🤖 助手: {assistant_msg.content}")

# ---------- 9. 测试 ----------
if __name__ == "__main__":
    print("=== Agentic RAG 演示（Agent 自主决定是否检索）===")

    # 场景1：知识库问题（应检索）
    ask("猫是什么？")

    # 场景2：知识库问题（应检索）
    ask("苹果是什么？")

    # 场景3：常识问题（无需检索）
    ask("1 + 1 等于几？")

    # 场景4：知识库问题（应检索）
    ask("北京是哪个国家的首都？")