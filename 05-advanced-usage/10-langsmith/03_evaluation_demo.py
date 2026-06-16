#!/usr/bin/env python3
"""LangSmith 评估演示 — 数据集驱动的测试"""

import requests
import json
import time

print("=" * 70)
print("LangSmith 评估演示 — 数据集驱动测试")
print("=" * 70)

# 1. 定义测试数据集
print("\n📋 [步骤1] 构建测试数据集")
test_dataset = [
    {"input": "Paris 的天气怎么样？", "expected_tool": "get_weather", "expected_city": "Paris"},
    {"input": "Python 的创始人是谁？", "expected_topic": "Python"},
    {"input": "GitHub 上最火的 LangChain 项目", "expected_tool": "search_github"},
]

print(f"  共 {len(test_dataset)} 条测试用例:")
for i, case in enumerate(test_dataset, 1):
    print(f"  {i}. {case['input'][:40]}...")

# 2. 模拟评估函数
print("\n🔍 [步骤2] 运行评估")
print("-" * 50)

def evaluate_tool_call(result: dict, expected: dict) -> dict:
    """评估工具调用是否准确"""
    messages = result.get("messages", [])
    if not messages:
        return {"score": 0, "reason": "无输出"}
    
    content = messages[-1].get("content", "")
    score = 0
    
    # 检查是否提到了预期城市/主题
    if "expected_city" in expected:
        if expected["expected_city"].lower() in content.lower():
            score = 1.0
        else:
            score = 0.5 if "天气" in content else 0.0
    elif "expected_topic" in expected:
        if expected["expected_topic"].lower() in content.lower():
            score = 0.8
        if content and len(content) > 50:
            score = min(score + 0.2, 1.0)
    
    return {"score": score, "prediction": content[:60]}

def evaluate_latency(start: float, end: float, threshold: float = 3.0) -> dict:
    """评估响应延迟"""
    latency = end - start
    return {"score": max(0, 1 - latency / threshold), "latency_sec": round(latency, 2)}

# 模拟评估
for case in test_dataset:
    start = time.time()
    
    # 模拟智能体调用
    if "tool" in case:
        time.sleep(0.2)
        result = {"messages": [{"content": f"正在查询{case.get('expected_city','')}的天气..."}]}
    else:
        time.sleep(0.3)
        result = {"messages": [{"content": f"{case.get('expected_topic','')}是一个重要的技术领域..."}]}
    
    end = time.time()
    
    # 评估
    tool_score = evaluate_tool_call(result, case)
    latency_score = evaluate_latency(start, end)
    
    print(f"\n  测试: {case['input'][:40]}")
    print(f"    工具调用评分: {tool_score['score']:.1f} ({tool_score['reason']})")
    print(f"    延迟: {latency_score['latency_sec']:.2f}s")

# 3. 汇总报告
print("\n📊 [步骤3] 汇总报告")
print("-" * 50)
print("""
  LangSmith 评估平台提供:
  
  1. 测试数据集管理
     • 创建/上传测试用例
     • 版本控制和对比
     • 自动生成测试数据
  
  2. 评估运行
     • 批量运行测试
     • 多维度评分 (正确性、工具调用、延迟)
     • 对比不同模型配置
  
  3. 回归检测
     • 自动检测性能退化
     • 历史基线对比
     • 告警通知
  
  4. 实际使用
     import langsmith
     client = langsmith.Client()
     
     results = client.evaluate(
         lambda inputs: agent.invoke(inputs),
         data="my-dataset",
         evaluators=[correctness, tool_call_accuracy]
     )
""")

print("=" * 70)
print("✅ 评估完成! 完整结果可查看 smith.langchain.com")
print("=" * 70)
