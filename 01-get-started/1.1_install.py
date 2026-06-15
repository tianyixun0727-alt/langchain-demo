#!/usr/bin/env python3
"""验证 LangChain 安装和环境配置"""

try:
    import langchain
    print(f"✅ LangChain version: {langchain.__version__}")
except ImportError:
    print("❌ LangChain not installed. Run: pip install langchain")
    exit(1)

try:
    from langchain_openai import ChatOpenAI
    print("✅ ChatOpenAI available (OpenAI-compatible API)")
except ImportError:
    print("⚠️  langchain_openai not available")

try:
    from langchain.agents import create_agent
    print("✅ create_agent available")
except ImportError:
    print("⚠️  create_agent not available")

print("\n✅ Environment is ready!")
print("Next step: python 02_quickstart.py")
