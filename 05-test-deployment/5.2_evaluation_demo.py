#!/usr/bin/env python3
"""评估 Demo — 真实智能体（仅天气工具）+ 自动评分"""

import time
from typing import Dict, Any
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# ========== 1. 定义工具 ==========
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息（模拟）"""
    return f"It's always sunny in {city}!"

# ========== 2. 创建智能体（仅天气工具） ==========
llm = ChatOpenAI(
    model="deepseek-v3",
    api_key="NbEJz6UO3LEL9uLngmohSK9iW8M2hNt8ZK5gn7MSq8trEplD",
    base_url="http://10.187.126.181:3000/v1"
)

agent = create_agent(
    model=llm,
    tools=[get_weather],               # 只保留天气工具
    system_prompt="You are a helpful assistant that can answer questions and use weather tool.",
)

# ========== 3. 辅助调用函数 ==========
def invoke_agent(query: str) -> Dict[str, Any]:
    """调用智能体，返回回答内容和延迟"""
    start = time.time()
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    latency = time.time() - start
    content = result["messages"][-1].content
    return {"content": content, "latency": latency}

# ========== 4. 构建测试数据集（包含天气和通用问题） ==========
dataset = [
    {"id": 1, "query": "What's the weather in San Francisco?", "category": "tool", "keywords": ["sunny", "San Francisco"], "min_length": 20},
    {"id": 2, "query": "What's the weather like in Beijing?", "category": "tool", "keywords": ["sunny", "Beijing"], "min_length": 20},
    {"id": 3, "query": "Python 中如何读取文件", "category": "code", "keywords": ["read", "file", "open"], "min_length": 50},
    {"id": 4, "query": "解释什么是 RAG", "category": "knowledge", "keywords": ["retrieval", "generation", "RAG"], "min_length": 80},
    {"id": 5, "query": "Docker 和虚拟机有什么区别", "category": "knowledge", "keywords": ["container", "VM", "virtual"], "min_length": 60},
]

print("=" * 70)
print("评估 Demo — 真实智能体（天气工具）+ 自动评分")
print("=" * 70)
print(f"\n📋 测试数据集: {len(dataset)} 条用例")
for d in dataset:
    print(f"  #{d['id']} [{d['category']}] {d['query'][:40]}")

# ========== 5. 运行评估 ==========
print("\n🔍 开始评估...\n")

results = []
for case in dataset:
    # 调用真实智能体
    resp = invoke_agent(case["query"])
    content = resp["content"]
    latency = resp["latency"]

    # 计算各项得分
    # (1) 关键词匹配得分 (0~1)
    content_lower = content.lower()
    keyword_hits = sum(1 for kw in case["keywords"] if kw.lower() in content_lower)
    keyword_score = min(1.0, keyword_hits / len(case["keywords"]))

    # (2) 长度得分 (至少 min_length 个字符)
    length = len(content)
    length_score = min(1.0, length / case["min_length"])

    # (3) 延迟得分 (要求低于2秒，否则扣分)
    latency_score = max(0, 1 - latency / 2.0)

    # 综合得分 (加权平均)
    total_score = (keyword_score * 0.5 + length_score * 0.3 + latency_score * 0.2)

    results.append({
        "id": case["id"],
        "query": case["query"],
        "score": total_score,
        "keyword_score": keyword_score,
        "length_score": length_score,
        "latency_score": latency_score,
        "latency": latency,
        "length": length,
    })

    # 打印每个用例的结果
    stars = "⭐" * int(total_score * 5)
    print(f"  #{case['id']} {case['query'][:30]:30s} {stars} {total_score:.2f} ({latency:.2f}s)")

# ========== 6. 汇总报告 ==========
print("\n📊 汇总报告")
print("-" * 50)
avg_score = sum(r["score"] for r in results) / len(results)
avg_latency = sum(r["latency"] for r in results) / len(results)
pass_count = sum(1 for r in results if r["score"] >= 0.6)
print(f"  平均综合得分: {avg_score:.2f}")
print(f"  平均延迟: {avg_latency:.2f}s")
print(f"  通过率 (≥0.6): {pass_count}/{len(results)}")
print(f"  状态: {'✅ 通过' if avg_score >= 0.7 else '⚠️ 需要优化'}")

# 可选：展示每个维度的平均分
print("\n📈 维度平均分:")
print(f"  关键词匹配: {sum(r['keyword_score'] for r in results)/len(results):.2f}")
print(f"  响应长度:   {sum(r['length_score'] for r in results)/len(results):.2f}")
print(f"  延迟:       {sum(r['latency_score'] for r in results)/len(results):.2f}")

print("\n" + "=" * 70)
print("LangSmith 评估集成")
print("=" * 70)
print("""
  在 LangSmith 中，你可以:
  
  1. 创建测试数据集
  client.create_dataset("my-agent-tests")
  client.create_examples(dataset=dataset_name, inputs=inputs, outputs=outputs)
  
  2. 运行评估
  results = client.evaluate(
      lambda inputs: agent.invoke(inputs),
      data=dataset_name,
      evaluators=[keyword_evaluator, length_evaluator, latency_evaluator],
  )
  
  3. 查看结果 → smith.langchain.com
""")