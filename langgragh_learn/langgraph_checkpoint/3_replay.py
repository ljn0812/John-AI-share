from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    value: int
    logs: list[str]


def node_a(state: State):

    print("执行 node_a")

    return {
        "value": state["value"] + 1,
        "logs": state["logs"] + ["node_a执行"]
    }


def node_b(state: State):

    print("执行 node_b")

    return {
        "value": state["value"] * 10,
        "logs": state["logs"] + ["node_b执行"]
    }


def node_c(state: State):

    print("执行 node_c")

    return {
        "value": state["value"] + 100,
        "logs": state["logs"] + ["node_c执行"]
    }


builder = StateGraph(State)


builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)


builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", "node_c")
builder.add_edge("node_c", END)


checkpointer = InMemorySaver()


graph = builder.compile(
    checkpointer=checkpointer
)

config = {
    "configurable": {
        "thread_id": "test-001"
    }
}
result = graph.invoke(
    {
        "value": 1,
        "logs": []
    },
    config=config
)
print(result)

history = list(graph.get_state_history(config))
for snapshot in history:
    print("====================")
    print(
        "checkpoint_id:",
        snapshot.config["configurable"]["checkpoint_id"]
    )
    print(
        "state:",
        snapshot.values
    )
    print(
        "next:",
        snapshot.next
    )

node_a_snapshot = history[2].config["configurable"]["checkpoint_id"]
print(node_a_snapshot)

print('-' * 50)

config = {
    "configurable": {
        "thread_id": "test-001",
        "checkpoint_id": node_a_snapshot
    }
}
result = graph.invoke(
    None,
    config=config
)
print(result)

