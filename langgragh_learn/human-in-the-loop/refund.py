from typing import TypedDict
from typing_extensions import NotRequired

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

# ============================================================
# 1. 定义 State
# ============================================================
class State(TypedDict):
    amount: int
    approved: NotRequired[bool]

# ============================================================
# 2. 定义节点
# ============================================================

def apply_refund(state: State):
    """准备退款"""
    print(f"准备退款：{state['amount']} 元")
    return {}


def human_review(state: State):
    """人工审批节点"""
    # 执行到这里，Graph 会暂停
    print(f"before: 人工审批 {state}")
    approved = True
    # approved = interrupt({
    #     "message": "退款金额较大，请人工审批",
    #     "amount": state["amount"]
    # })
    print(f"after: 人工审批 {approved} {state}")

    # 只有调用 Command(resume=...) 后，
    # 才会继续执行到这里
    return {
        "approved": approved
    }


def execute_refund(state: State):
    """真正执行退款"""

    if state["approved"]:
        print("审批通过，执行退款")
        print(f"成功退款：{state['amount']} 元")
    else:
        print("审批拒绝，不执行退款")
    return {}


# ============================================================
# 3. 创建 Graph
# ============================================================

builder = StateGraph(State)

builder.add_node("apply_refund", apply_refund)
builder.add_node("human_review", human_review)
builder.add_node("execute_refund", execute_refund)

builder.add_edge(START, "apply_refund")
builder.add_edge("apply_refund", "human_review")
builder.add_edge("human_review", "execute_refund")
builder.add_edge("execute_refund", END)


# ============================================================
# 4. 配置 Checkpointer
# ============================================================

# checkpointer = InMemorySaver()
from json_file_saver import JsonFileSaver
checkpointer = JsonFileSaver("checkpoint.json")

graph = builder.compile(
    checkpointer=checkpointer
)


# ============================================================
# 5. 配置 thread_id
# ============================================================

config = {
    "configurable": {
        "thread_id": "refund-001"
    }
}


# ============================================================
# 6. 第一次执行
# ============================================================

# result = graph.invoke(
#     {
#         "amount": 5000
#     },
#     config=config
# )

for idx, snapshot in enumerate(graph.get_state_history(config)):
    print(idx, snapshot)
# """
# {'amount': 5000, '__interrupt__': [Interrupt(value={'message': '退款金额较大，请人工审批', 'amount': 5000}, id='543edf01c94fb745185e07498d9f60ff')]}
# """


# ============================================================
# 7. 判断是否进入人工审批
# ============================================================
print("\n请选择：")
print("1. 同意退款")
print("2. 拒绝退款")

# ========================================================
# 8. 等待人工输入
# ========================================================
while True:
    choice = input("\n请输入 1 或 2：").strip()
    if choice == "1":
        approved = True
        print("\n人工操作：同意退款")
        break
    elif choice == "2":
        approved = False
        print("\n人工操作：拒绝退款")
        break

    else:
        print("输入错误，请输入 1 或 2")

# ========================================================
# 9. 恢复 Graph
# ========================================================

result = graph.invoke(
    Command(resume=approved),
    config=config
)

# ============================================================
# 10. 输出最终状态
# ============================================================

print("\n==============================")
print("          最终结果")
print("==============================")

print(result)
print("长度", len(list(graph.get_state_history(config))))
for idx, snapshot in enumerate(graph.get_state_history(config)):
    print(idx, snapshot)