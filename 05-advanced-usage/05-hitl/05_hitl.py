#!/usr/bin/env python3
"""人机协作 (HITL) — 敏感操作人工审批"""

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ToolCallRequest
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-dac290dd70064370ac10057fdcee7f08",
    base_url="https://api.deepseek.com"
)

@tool
def execute_sql(query: str) -> str:
    """执行 SQL 查询"""
    return f"已执行 SQL: {query}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件"""
    return f"邮件已发送至 {to}: {subject}"

@tool
def read_file(path: str) -> str:
    """读取本地文件"""
    return f"模拟读取文件: {path}"

# 条件中断: 只中断写操作，不中断读操作
def is_write_query(request: ToolCallRequest) -> bool:
    """只有 DELETE/DROP/UPDATE 才需要审批"""
    query = request.tool_call.args.get("query", "").upper()
    return any(kw in query for kw in ["DELETE", "DROP", "UPDATE"])

agent = create_agent(
    llm=llm,
    tools=[execute_sql, send_email, read_file],
    middleware=[HumanInTheLoopMiddleware(
        interrupt_on={
            # 允许所有决策类型 (approve/edit/reject/respond)
            "send_email": True,
            # 只允许审批和拒绝，不允许编辑
            "execute_sql": {
                "allowed_decisions": ["approve", "reject"],
                "when": is_write_query,  # 条件中断
            },
            # 安全操作，不需要审批
            "read_file": False,
        },
        description_prefix="需要人工审批",
    )],
    checkpointer=InMemorySaver(),
)

print("=" * 70)
print("人机协作 (HITL) — 完整演示")
print("=" * 70)

print("""
四种审批决策类型:
""")

print(f"{'决策类型':<12} {'说明':<28} {'示例场景'}")
print("-" * 70)
print(f"{'approve':<12} {'批准执行，不修改':<28} {'按草稿发送邮件'}")
print(f"{'edit':<12} {'修改参数后执行':<28} {'更改收件人后发送'}")
print(f"{'reject':<12} {'拒绝执行，附理由':<28} {'拒绝删除文件并解释'}")
print(f"{'respond':<12} {'跳过工具，直接回复':<28} {'回答'询问用户'类工具'}")

print()
print("=" * 70)
print("工作流程")
print("=" * 70)
print("""
  用户提问
     ↓
  ┌─────────────────────────────────────┐
  │        智能体推理                     │
  │  调用工具 → HITL 中间件              │
  └─────────────────────────────────────┘
     ↓
  ┌─────────────────────────────────────┐
  │  HITL 检查: 此工具需要审批吗？        │
  │  ├─ 不需要 → 直接执行                │
  │  └─ 需要 → 暂停执行，等待人工决策     │
  │                                      │
  │  决策类型:                            │
  │  ├─ approve  → 按原参数执行           │
  │  ├─ edit     → 修改参数后执行         │
  │  ├─ reject   → 拒绝，加入解释到对话   │
  │  └─ respond  → 人工回复替代工具结果   │
  └─────────────────────────────────────┘
     ↓
  智能体继续 → 最终回复
""")

print("=" * 70)
print("使用示例")
print("=" * 70)
print()

print("场景: 用户要求删除数据库中的数据")
print("-" * 50)

# 模拟第一次调用——会被 HITL 中断
import time
print("\n🔄 [第1步] 智能体收到请求，调用 execute_sql...")
print("   → HITL 检测到 DELETE 操作，触发中断!")
print("   → 状态已保存到检查点 (thread-1)")
print("\n⏸️  执行暂停，等待人工决策...")
print("    决策选项: approve | reject")
print()

# 模拟人工决策
print("👤 [第2步] 人工审批:")
print("   → 决策: reject")
print("   → 理由: '不允许删除生产数据'")
print()

print("🔄 [第3步] 继续执行:")
print("   → HITL 收到 reject 决策")
print("   → 拒绝理由被加入对话")
print("   → 智能体继续推理")
print()

print("✅ HITL 工作流完成!")
print()

print("=" * 70)
print("配置说明")
print("=" * 70)
print("""
interrupt_on 配置:
  "send_email": True          → 所有调用都需要审批
  "execute_sql": {            → 只审批写操作
      "allowed_decisions": ["approve", "reject"],
      "when": is_write_query  # 条件判断
  }
  "read_file": False          → 自动放行

注意:
  1. HITL 需要 checkpointer 来保存中断状态
  2. 生产环境使用 AsyncPostgresSaver
  3. 每次调用需要传入 thread_id
  4. 多个工具同时中断时，需按顺序分别决策

实际恢复执行的代码:
  # 从检查点恢复
  config = {"configurable": {"thread_id": "thread-1"}}
  state = checkpointer.get(config)
  
  # 人工决策
  decisions = [{"type": "reject", "reason": "不允许删除生产数据"}]
  
  # 继续执行
  result = agent.invoke(None, config, interrupt_decisions=decisions)
""")
