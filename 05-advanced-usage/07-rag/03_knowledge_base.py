#!/usr/bin/env python3
"""知识库构建 — 从真实数据源构建可搜索知识库"""

import requests
import json
from typing import List, Dict

print("=" * 60)
print("知识库构建完整流程")
print("=" * 60)

# 1. 数据加载 (Document Loader)
print("\n📥 步骤1: 加载数据 (Document Loading)")
print("-" * 40)

# 从 GitHub API 加载真实项目数据
print("从 GitHub API 加载热门 AI 项目数据...")
try:
    resp = requests.get(
        "https://api.github.com/search/repositories?q=topic:llm&sort=stars&per_page=10",
        headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )
    repos = resp.json().get("items", [])
    print(f"  ✅ 成功加载 {len(repos)} 个开源项目")
except Exception as e:
    print(f"  ⚠️ 加载失败: {e}")
    repos = []

# 2. 文本分块 (Text Splitting)
print("\n✂️ 步骤2: 文本分块 (Text Splitting)")
print("-" * 40)
documents = []
for r in repos:
    repo_doc = {
        "name": r["full_name"],
        "description": r.get("description", ""),
        "language": r.get("language", ""),
        "stars": r["stargazers_count"],
        "url": r["html_url"],
        "topics": r.get("topics", []),
    }
    documents.append(repo_doc)

# 模拟分块
chunk_size = 3
chunks = [documents[i:i+chunk_size] for i in range(0, len(documents), chunk_size)]
print(f"  📄 共 {len(documents)} 条文档")
print(f"  ✂️ 分成 {len(chunks)} 个块 (每块 {chunk_size} 条)")
print(f"  📏 块大小: ~200 tokens/块")

# 3. 向量化 (Embedding)
print("\n🧬 步骤3: 向量化 (Embedding)")
print("-" * 40)
print("""
  示例:
  from langchain.embeddings import init_embeddings
  embeddings = init_embeddings("openai:text-embedding-3-small")
  
  将文本 → [0.023, -0.456, 0.789, ...] (1536维向量)
""")

# 4. 存入向量数据库
print("\n💾 步骤4: 存入向量数据库 (Vector Store)")
print("-" * 40)
print("""
  from langchain.vectorstores import InMemoryVectorStore
  vector_store = InMemoryVectorStore(embeddings)
  vector_store.add_documents(chunks)
  
  生产环境: Chroma / Pinecone / Weaviate / Qdrant
""")

# 5. 检索
print("\n🔍 步骤5: 检索 (Retrieval)")
print("-" * 40)

def simple_search(docs: List[Dict], query: str) -> List[Dict]:
    """简单关键词检索演示"""
    query = query.lower()
    results = []
    for d in docs:
        score = 0
        if query in d["name"].lower():
            score += 3
        if query in d["description"].lower():
            score += 2
        if query in " ".join(d["topics"]).lower():
            score += 2
        if score > 0:
            results.append((score, d))
    results.sort(reverse=True)
    return [d for s, d in results[:3]]

# 演示检索
query = "language model"
results = simple_search(documents, query)
print(f'  查询: "{query}"')
print(f'  匹配到 {len(results)} 条结果:')
for r in results:
    print(f'    • {r["name"]} ⭐{r["stars"]}')
    if r.get("description"):
        print(f'      {r["description"][:80]}')
print()

# 6. 生成 (Generation)
print("🤖 步骤6: 生成 (Generation)")
print("-" * 40)
print("""
  结合检索结果 + 用户问题 → LLM 生成答案
  
  from langchain.agents import create_agent
  
  @tool
  def search_knowledge_base(query: str) -> str:
      \"\"\"搜索知识库\"\"\"
      results = vector_store.similarity_search(query, k=3)
      return "\\n\\n".join(d.page_content for d in results)
  
  agent = create_agent(llm=llm, tools=[search_knowledge_base])
""")

print("=" * 60)
print("✅ 知识库构建完成！")
print("=" * 60)
