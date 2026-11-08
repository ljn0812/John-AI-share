from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# =========================================================
# 1. 定义状态
# =========================================================

class State(TypedDict):
    message: str


# =========================================================
# 2. 构建子图
# =========================================================

def subgraph_node_1(state: State):
    return {
        "message": state["message"] + " -> 子图步骤1"
    }


def subgraph_node_2(state: State):
    return {
        "message": state["message"] + " -> 子图步骤2"
    }


subgraph_builder = StateGraph(State)

subgraph_builder.add_node(
    "subgraphNode1",
    subgraph_node_1
)

subgraph_builder.add_node(
    "subgraphNode2",
    subgraph_node_2
)

subgraph_builder.add_edge(
    START,
    "subgraphNode1"
)

subgraph_builder.add_edge(
    "subgraphNode1",
    "subgraphNode2"
)

subgraph_builder.add_edge(
    "subgraphNode2",
    END
)

subgraph = subgraph_builder.compile()
# =========================================================
# 3. 构建父图
# =========================================================

def parent_node(state: State):
    return {
        "message": state["message"] + " -> 父图处理"
    }


builder = StateGraph(State)

builder.add_node(
    "parentNode",
    parent_node
)

# 重点：
# 直接把编译后的子图作为一个 Node
builder.add_node(
    "subgraph",
    subgraph
)

builder.add_edge(
    START,
    "parentNode"
)

builder.add_edge(
    "parentNode",
    "subgraph"
)

builder.add_edge(
    "subgraph",
    END
)

graph = builder.compile()


# =========================================================
# 4. 执行
# =========================================================

result = graph.invoke({
    "message": "用户请求"
})

print(result)