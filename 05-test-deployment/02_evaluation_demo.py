#!/usr/bin/env python3
"""评估 Demo — 真实数据集 + 评分演示"""

import requests
import time
import json

print("=" * 70)
print("评估 Demo — 真实数据集 + 自动评分")
print("=" * 70)

# 构建测试数据集
dataset = [
    {"id": 1, "query": "Python 中如何读取文件", "category": "code", "min_length": 50},
    {"id": 2, "query": "解释什么是 RAG", "category": "knowledge", "min_length": 80},
    {"id": 3, "query": "Docker 和虚拟机有什么区别", "category": "knowledge", "min_length": 60},
    {"id": 4, "query": "用 Python 写一个快排", "category": "code", "min_length": 100},
]

print(f"📋 测试数据集: {len(dataset)} 条用例")
for d in dataset:
    print(f"  #{d['id']} [{d['category']}] {d['query'][:40]}")

# 模拟评估
print("\n🔍 开始评估...\n")

results = []
for case in dataset:
    start = time.time()
    
    # 模拟智能体调用 + 网络请求
    if case["category"] == "code":
        time.sleep(0.4)
        mock_response = f"以下是关于 {case['query']} 的解答...\n\n```python\n# 示例代码\nwith open('file.txt', 'r') as f:\n    content = f.read()\n    print(content)\n```"
    else:
        time.sleep(0.3)
        mock_response = f"{case['query']} 是指..."
    
    end = time.time()
    latency = end - start
    
    # 计算评分
    response_length = len(mock_response)
    length_score = min(1.0, response_length / case["min_length"])
    latency_score = max(0, 1 - latency / 2.0)
    total_score = (length_score * 0.5 + latency_score * 0.5)
    
    results.append({
        "id": case["id"],
        "query": case["query"],
        "score": total_score,
        "latency": latency,
        "length": response_length,
    })
    
    stars = "⭐" * int(total_score * 5)
    print(f"  #{case['id']} {case['query'][:30]:30s} {stars} {total_score:.2f} ({latency:.1f}s)")

# 汇总
print("\n📊 汇总报告")
print("-" * 50)
avg_score = sum(r["score"] for r in results) / len(results)
avg_latency = sum(r["latency"] for r in results) / len(results)
print(f"  平均评分: {avg_score:.2f}")
print(f"  平均延迟: {avg_latency:.2f}s")
print(f"  通过率: {sum(1 for r in results if r['score'] >= 0.6)}/{len(results)}")
print(f"  状态: {'✅ 通过' if avg_score >= 0.7 else '⚠️ 需要优化'}")

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
      evaluators=[correctness_evaluator],
  )
  
  3. 查看结果 → smith.langchain.com
""")
