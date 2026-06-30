from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

try:
    collections = client.get_collections()
    print("✅ Qdrant 连接成功！")
    print(f"当前已有的 collection: {collections}")
except Exception as e:
    print(f"❌ 连接失败: {e}")