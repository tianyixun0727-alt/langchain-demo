#!/usr/bin/env python3
"""自定义工作流 — LangGraph 风格的可运行流水线"""

import requests
import json
import time

print("=" * 70)
print("自定义工作流 — GitHub 项目搜索 + 分析流水线")
print("=" * 70)

# 定义状态
state = {
    "query": "langchain",
    "search_results": [],
    "stats": {},
    "report": "",
}

def step1_search(state: dict) -> dict:
    """步骤1: 搜索 GitHub 项目"""
    print(f"\n🔍 [步骤1] 搜索: {state['query']}")
    try:
        resp = requests.get(
            f"https://api.github.com/search/repositories?q={state['query']}&sort=stars&per_page=5",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        items = resp.json().get("items", [])
        results = []
        for r in items:
            results.append({
                "name": r["full_name"],
                "stars": r["stargazers_count"],
                "lang": r.get("language") or "未知",
                "desc": r.get("description") or "无描述",
                "url": r["html_url"],
            })
        state["search_results"] = results
        print(f"  找到 {len(results)} 个项目")
        return state
    except Exception as e:
        print(f"  搜索失败: {e}")
        return state

def step2_analyze(state: dict) -> dict:
    """步骤2: 分析搜索结果"""
    print(f"\n📊 [步骤2] 分析搜索结果")
    results = state["search_results"]
    if not results:
        print("  无数据可分析")
        return state
    
    stats = {
        "total": len(results),
        "total_stars": sum(r["stars"] for r in results),
        "languages": {},
    }
    for r in results:
        lang = r["lang"]
        stats["languages"][lang] = stats["languages"].get(lang, 0) + 1
    
    state["stats"] = stats
    print(f"  项目数: {stats['total']}")
    print(f"  总星标: {stats['total_stars']:,}")
    print(f"  编程语言分布: {stats['languages']}")
    return state

def step3_report(state: dict) -> dict:
    """步骤3: 生成报告"""
    print(f"\n📝 [步骤3] 生成报告")
    report = f"=== GitHub 项目报告: {state['query']} ===\n\n"
    
    for r in state["search_results"]:
        report += (
            f"📦 {r['name']}\n"
            f"   ⭐ {r['stars']:,}  |  💻 {r['lang']}\n"
            f"   📄 {r['desc'][:80]}\n"
            f"   🔗 {r['url']}\n\n"
        )
    
    if state.get("stats"):
        s = state["stats"]
        report += f"--- 统计 ---\n"
        report += f"总计 {s['total']} 个项目, ⭐ {s['total_stars']:,}\n"
    
    state["report"] = report
    print("  报告已生成")
    return state

# 执行工作流
print("\n=== 开始执行流水线 ===\n")

for step in [step1_search, step2_analyze, step3_report]:
    print(f"▶ 执行: {step.__name__}")
    state = step(state)
    time.sleep(0.5)

print("\n" + "=" * 70)
print("最终报告")
print("=" * 70)
print(state["report"])

print("\n" + "=" * 70)
print("工作流说明")
print("=" * 70)
print("""
这个流水线模拟了 LangGraph 的执行模式:

  START
    ↓
  [search]  — 搜索 GitHub API, 获取原始数据
    ↓
  [analyze] — 统计数据, 分析语言分布
    ↓
  [report]  — 生成结构化报告
    ↓
  END

实际 LangGraph 代码:
  from langgraph.graph import StateGraph, START
  graph = StateGraph(SearchState)
  graph.add_node("search", search_node)
  graph.add_node("analyze", analyze_node)
  graph.add_node("report", report_node)
  graph.add_edge(START, "search")
  graph.add_edge("search", "analyze")
  graph.add_edge("analyze", "report")
  chain = graph.compile()
  result = chain.invoke({"query": "langchain"})
""")
