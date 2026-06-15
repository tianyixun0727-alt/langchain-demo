#!/usr/bin/env python3
"""RAG Overview — Three architectures compared"""

print("""
============================================
RAG — Retrieval-Augmented Generation
============================================

LLM 有两个关键限制：
  1. 有限的上下文 — can't ingest entire corpora at once
  2. 静态知识 — training data is frozen in time

RAG addresses these by fetching relevant external knowledge at query time.

Three RAG Architectures
-----------------------
""")

print("Architecture      | Description                          | Control | Latency")
print("------------------|--------------------------------------|---------|--------")
print("1. 2-Step RAG     | Retrieval before generation          | High    | Fast")
print("2. Agentic RAG    | Agent decides when to retrieve       | Low     | Variable")
print("3. Hybrid RAG     | Both approaches with validation      | Medium  | Variable")
print()

print("""
2-Step RAG (Simple & Predictable)
  Retrieval always happens before generation.
  Suitable for FAQs, documentation bots, simple Q&A.

Agentic RAG (Flexible & Powerful)
  An LLM-powered agent decides WHEN to retrieve during reasoning.
  The agent has access to one or more tools that fetch knowledge.
  Suitable for research assistants, complex analysis.

Hybrid RAG (Balanced)
  Combines characteristics of both approaches with validation.
  Suitable for domain-specific Q&A with quality checks.

Building Blocks
---------------
  1. Document Loaders — Ingest from PDF, web, databases
  2. Text Splitters — Break into chunks that fit context windows
  3. Embedding Models — Convert text to vectors
  4. Vector Stores — Store and search embeddings
  5. Retrievers — Return documents given an unstructured query

See the sub-files for runnable demos:
  python 02_agentic_rag.py
  python 03_knowledge_base.py
""")
