#!/usr/bin/env python3
"""两步法 RAG（Qdrant 版本，原生 score_threshold 过滤）"""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

# ------------------- 1. 初始化模型 -------------------
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

# ------------------- 2. 读取知识库 -------------------
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

# ------------------- 3. 删除已有 collection（若有） -------------------
COLLECTION_NAME = "rag_docs_2step"
client = QdrantClient(host="localhost", port=6333)
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    print(f"🗑️  已删除旧 collection: {COLLECTION_NAME}")

# ------------------- 4. 创建向量库（使用 location 参数） -------------------
vectorstore = Qdrant.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    collection_name=COLLECTION_NAME,
    distance_func="Cosine",
    location="localhost:6333",  # ✅ 使用 location 让库内部创建客户端
)
print(f"✅ 向量库已就绪（Qdrant, collection: {COLLECTION_NAME}）")

# ------------------- 5. 检索函数（使用原生 score_threshold） -------------------
def retrieve(query, k=5, threshold=0.7):
    docs_with_score = vectorstore.similarity_search_with_score(
        query=query,
        k=k,
        score_threshold=threshold
    )
    results = []
    for doc, score in docs_with_score:
        results.append({
            "id": doc.metadata.get("id", "未知"),
            "content": doc.page_content,
            "score": score
        })
    return results

# ------------------- 6. 用户问题 -------------------
user_question = "苹果是一种常见的水果，味道甜美，富含维生素C"
print(f"\n👤 用户: {user_question}")

retrieved = retrieve(user_question, k=10, threshold=0.5)

if not retrieved:
    print("❌ 未找到相关文档。")
    exit()

print("\n📄 检索到的文档:")
for idx, doc in enumerate(retrieved, 1):
    preview = doc["content"][:40] + "..." if len(doc["content"]) > 40 else doc["content"]
    print(f"  {idx}. [ID: {doc['id']}] (相似度: {doc['score']:.3f}) {preview}")

# ------------------- 7. 生成答案 -------------------
context = "\n".join([doc["content"] for doc in retrieved])
system_msg = f"你是一个智能助手，请基于以下参考文档回答用户问题。如果文档中没有相关信息，请明确告知用户。\n\n参考文档：\n{context}"

messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_question}
]

response = llm.invoke(messages)
print(f"\n🤖 助手: {response.content}")