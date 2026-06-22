#!/usr/bin/env python3
"""
LangChain 0.3 + LangGraph 环境检测
"""

# =========================
# 需要安装的依赖（必须）
# =========================
# pip install langchain
# pip install langchain-openai
# pip install langchain-core
# pip install langgraph
# pip install langchain-community   # （可选扩展）
# pip install openai
# pip install tiktoken


# =========================
# 1. LangChain
# =========================
def check_langchain():
    try:
        import langchain
        print(f"✅ LangChain version: {langchain.__version__}")
    except ImportError:
        print("❌ LangChain 未安装")


# =========================
# 2. OpenAI 适配包（只检查安装）
# =========================
def check_openai():
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain-openai 已安装")
    except ImportError:
        print("❌ langchain-openai 未安装")


# =========================
# 3. Core（LCEL + Tool）
# =========================
def check_core():
    try:
        from langchain_core.tools import tool
        print("✅ langchain-core (Tool) 可用")
    except ImportError:
        print("❌ langchain-core 未安装")

    try:
        from langchain_core.prompts import ChatPromptTemplate
        print("✅ langchain-core (Prompt/LCEL) 可用")
    except ImportError:
        print("❌ Prompt 模块不可用")


# =========================
# 4. LangGraph
# =========================
def check_langgraph():
    try:
        from langgraph.graph import StateGraph
        print("✅ LangGraph 已安装（Graph Agent 可用）")
    except ImportError:
        print("❌ langgraph 未安装")


# =========================
# 5. Tool 运行测试
# =========================
def check_tools_runtime():
    try:
        from langchain_core.tools import tool

        @tool
        def add(a: int, b: int) -> int:
            """计算两个数的和"""
            return a + b

        result = add.invoke({"a": 2, "b": 3})

        print(f"✅ Tool 运行正常：2 + 3 = {result}")

    except Exception as e:
        print(f"❌ Tool 运行失败：{e}")


# =========================
# 6. Main
# =========================
def main():
    print("===================================")
    print(" LangChain Environment Check")
    print("===================================\n")

    check_langchain()
    check_openai()
    check_core()
    check_langgraph()
    check_tools_runtime()

    print("\n===================================")
    print("✅ 环境检查完成")
    print("===================================")


if __name__ == "__main__":
    main()