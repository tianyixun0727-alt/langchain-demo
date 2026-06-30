#!/usr/bin/env python3
"""证券法规问答 Agent（综合 RAG 演示）
   功能：
   - 加载 Word 法规文档
   - 按章节分割并向量化（Qdrant + bge-m3 嵌入）
   - 提供检索工具，供 Agent 调用
   - Agent 根据用户问题自主决定是否检索，并严格按照法规条文回答
"""
#uv pip install langchain-openai langchain-qdrant qdrant-client langchain-community docx2txt
#uv pip install langchain-text-splitters
#uv pip install langchain-core

#“重大资产重组的认定标准有哪些？”
#“发行股份购买资产需要满足什么条件？”
#“上市公司重大资产重组的信息披露有什么要求？”
#“违反重组规定会面临什么法律责任？”
#“股东大会审议重大资产重组需要多少表决权通过？”

import os
import re
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.agents import create_agent
from langchain.tools import tool

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

# ---------- 2. 加载并分割文档（按章节+长度分割） ----------
def load_and_split_document(file_path: str) -> List[Document]:
    """
    1. 加载 Word 文档
    2. 尝试按 "### =<章节>" 分割成章节块
    3. 如果分割失败，回退到整篇分割
    """
    loader = Docx2txtLoader(file_path)
    raw_docs = loader.load()
    if not raw_docs:
        raise ValueError("文档加载为空，请检查文件是否可读。")
    full_text = raw_docs[0].page_content
    print(f"📄 文档总字符数: {len(full_text)}")
    print(f"📄 文档前 200 字符预览:\n{full_text[:200]}...\n")

    # 尝试按章节标记分割
    lines = full_text.split('\n')
    chapters = []
    current_chapter = None
    current_content = []

    # 识别以 "### =<章节>" 开头的行
    chapter_pattern = re.compile(r'^###\s*=\s*<章节>.*$')

    for line in lines:
        if chapter_pattern.match(line.strip()):
            # 保存上一个章节
            if current_chapter is not None:
                chapters.append((current_chapter, '\n'.join(current_content).strip()))
            current_chapter = line.strip()
            current_content = []
        else:
            if current_chapter is not None:
                current_content.append(line)
            # 忽略开头没有章节标记的内容（如标题、颁布信息等）
    # 添加最后一个章节
    if current_chapter is not None:
        chapters.append((current_chapter, '\n'.join(current_content).strip()))

    print(f"📂 成功识别章节数: {len(chapters)}")

    # 如果识别不到任何章节，则直接使用整篇作为单一文档
    if not chapters:
        print("⚠️ 未识别到章节标记，将使用整篇文档分割。")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "；", "，", " ", ""],
            length_function=len,
        )
        chunks = splitter.split_text(full_text)
        final_docs = []
        for chunk in chunks:
            final_docs.append(Document(
                page_content=chunk,
                metadata={"chapter": "全文"}
            ))
        return final_docs

    # 提取章节号（用于元数据）
    def extract_chapter_number(header: str) -> str:
        match = re.search(r'<章节>\s*(.*?)$', header)
        if match:
            return match.group(1).strip()
        return "未知章节"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "；", "，", " ", ""],
        length_function=len,
    )

    final_docs = []
    for header, content in chapters:
        chapter_num = extract_chapter_number(header)
        chunks = splitter.split_text(content)
        for chunk in chunks:
            final_docs.append(Document(
                page_content=chunk,
                metadata={"chapter": chapter_num}
            ))

    return final_docs


# ---------- 3. 构建向量库 ----------
file_path = os.path.join(os.path.dirname(__file__), "《上市公司重大资产重组管理办法（2023年修订）》2023-02-17发布-现行有效.docx")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"请将法规文档放在 {file_path}")

print("📄 正在加载并分割文档...")
docs = load_and_split_document(file_path)
print(f"✅ 文档分割为 {len(docs)} 个向量块")

print("🧠 正在构建向量库...")

# ----- 新增：Qdrant 客户端和 collection 管理 -----
COLLECTION_NAME = "regulations_agentic"
client = QdrantClient(host="localhost", port=6333)
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    print(f"🗑️  已删除旧 collection: {COLLECTION_NAME}")

vectorstore = Qdrant.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    distance_func="Cosine",
    location="localhost:6333",
)
# 获取向量数量
points_count = vectorstore.client.get_collection(COLLECTION_NAME).points_count
print(f"📊 向量库构建完成，共 {points_count} 条向量")

# 检索函数（用于工具）
def retrieve_documents(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """检索最相关的文档块，返回包含内容和章节元数据的列表"""
    # 不传入 score_threshold，与 Chroma 行为一致（不过滤）
    results = vectorstore.similarity_search_with_score(query, k=k)
    output = []
    for doc, score in results:
        output.append({
            "content": doc.page_content,
            "chapter": doc.metadata.get("chapter", "未知章节"),
            "score": score
        })
    return output


# ---------- 4. 定义 agent 工具 ----------
@tool
def search_regulations(query: str) -> str:
    """
    在《上市公司重大资产重组管理办法》中搜索与问题相关的条文。
    当用户询问关于重大资产重组、发行股份购买资产、重组程序、信息披露、监督管理等法规内容时，必须使用此工具。
    返回最相关的条文片段及其所属章节。
    """
    results = retrieve_documents(query, k=3)
    if not results:
        return "知识库中未找到相关条文。"
    
    formatted = []
    for item in results:
        chapter = item["chapter"]
        content = item["content"]
        formatted.append(f"【{chapter}】\n{content}")
    
    return "\n\n---\n\n".join(formatted)


# ---------- 5. 创建 Agent（设定系统提示词） ----------
system_prompt = """# 角色
你是一位资深且权威的证券行业法律法规专家，对各类相关条文不仅了如指掌，还能迅速、精准且全面地检索并运用条文，为复杂的法律法规咨询提供详尽、清晰且易懂的专业解答。

## 技能
### 技能 1: 问题答案检索
1. 当收到问题检索请求时，在知识库<证券法律法规制度>中迅速且精确地查找对应的法律法规条文，确保条文完整且准确无误。
    - 严格把控检索条文的质量，杜绝任何错误或不完整的情况出现。
    - 若知识库的搜索结果显示"没有检索到相关条文"或无内容，及时告知用户无法找到相关条文或制度。
2. 从知识库获取有效内容后，对用户的法律法规咨询进行深入且全面的剖析与理解。
    - 准确提取检索内容中"<章节>"后的具体章节或者条目信息至<chapter>。例如"第五条"，"第一章"
    - 凭借检索的条文和深厚的专业知识，给出准确、清晰、简明易懂的解答，并在回答后追加："具体章节：<chapter>"。如果存在多个<章节>的引用，则显示所有引用章节。
    - 若<chapter>为空或'未明确章节'，或者未找到相关条文或制度，明确告知用户无法找到相关条文或制度。
### 技能 2: 修正用户问题
1. 若<chapter>为空或未明确章节，清晰告知用户无法找到相关条文或制度。
2. 若知识库搜索无果，如实告知用户无法找到相关条文或制度。
## 限制
- 仅依据知识库的内容进行回答，不处理知识库范围外的问题。
- 只专注处理与证券行业外部法律法规紧密相关的内容，坚决拒绝无关话题。
- 所有解答都要以准确的条文和专业知识为基础，严禁随意猜测。

## 重要提示
- 当你需要检索时，必须调用 search_regulations 工具。
- 如果问题涉及上述法规内容，务必先检索再回答。
- 如果问题不涉及该法规或超出知识库范围，应礼貌拒绝并说明。
"""

# 创建 Agent
agent = create_agent(
    model=llm,
    tools=[search_regulations],
    system_prompt=system_prompt,
)

# ---------- 6. 交互式问答 ----------
def ask_question(question: str):
    print(f"\n❓ 用户: {question}")
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    answer = result["messages"][-1].content
    print(f"🤖 助手: {answer}")

if __name__ == "__main__":
    print("=== 证券法规问答 Agent（基于《上市公司重大资产重组管理办法》）===")
    print("输入 'quit' 退出\n")
    
    while True:
        user_input = input("请输入您的问题: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        if not user_input:
            continue
        ask_question(user_input)