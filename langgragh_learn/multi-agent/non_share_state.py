from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# =========================================================
# 1. 定义子图状态
# =========================================================

class SubgraphState(TypedDict):
    content: str


def subgraph_node_1(state: SubgraphState):
    return {
        "content": state["content"] + " -> 子图处理步骤1"
    }


def subgraph_node_2(state: SubgraphState):
    return {
        "content": state["content"] + " -> 子图处理步骤2"
    }


# =========================================================
# 2. 构建子图
# =========================================================
subgraph_builder = StateGraph(SubgraphState)

subgraph_builder.add_node("subgraphNode1", subgraph_node_1)
subgraph_builder.add_node("subgraphNode2", subgraph_node_2)

subgraph_builder.add_edge(START, "subgraphNode1")
subgraph_builder.add_edge("subgraphNode1", "subgraphNode2")
subgraph_builder.add_edge("subgraphNode2", END)

subgraph = subgraph_builder.compile()
# =========================================================
# 3. 定义父图状态
# =========================================================

class ParentState(TypedDict):
    message: str


# =========================================================
# 4. 父图节点
# =========================================================

def node_1(state: ParentState):
    return {
        "message": state["message"] + " -> 父图处理"
    }


def node_2(state: ParentState):

    # 1. 父图状态 -> 子图状态
    subgraph_input = {
        "content": state["message"]
    }

    # 2. 调用子图
    response = subgraph.invoke(subgraph_input)

    # 3. 子图状态 -> 父图状态
    return {
        "message": response["content"]
    }


# =========================================================
# 5. 构建父图
# =========================================================

builder = StateGraph(ParentState)

builder.add_node("node1", node_1)
builder.add_node("node2", node_2)

builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", END)

graph = builder.compile()


# =========================================================
# 6. 执行父图
# =========================================================

result = graph.invoke({
    "message": "用户请求"
})

print(result)