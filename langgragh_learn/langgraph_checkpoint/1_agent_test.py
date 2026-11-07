from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from agent import create_agent
from langchain_core.messages import HumanMessage


@tool
def get_weather(location: str) -> str:
    """查询天气信息"""
    return f"今天{location}的温度是 100℃"

@tool
def multiply(a: int, b: int) -> str:
    """将 a 和 b 相乘"""
    return str(a * b)


model = ChatTongyi(model="qwen3-max")
tools = [get_weather, multiply]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个智能助手，可以查询天气和进行数学计算。"
)

# ValueError: Checkpointer requires one or more of the following 'configurable' keys: thread_id, checkpoint_ns, checkpoint_id
config = {
    "configurable": {
        "thread_id": "session_1"
    }
}
result = agent.invoke({
    "messages": [HumanMessage(content='你好，我是阿苑')],
    },
    config=config
)
print("助手:", result['messages'][-1].content)
#------------ checkpoint -------------------
# state_snapshot = agent.get_state(config)
# print(f"备份1：{state_snapshot.values}")
"""
备份：{'messages': 
[HumanMessage(content='你好，我是阿苑', additional_kwargs={}, response_metadata={}), 
AIMessage(content='你好，阿苑！有什么我可以帮你的吗？', additional_kwargs={}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'stop', 'request_id': '1d338193-550d-9a3b-80f2-33ce5896a2b7', 'token_usage': {'input_tokens': 336, 'output_tokens': 11, 'prompt_tokens_details': {'cached_tokens': 0}, 'total_tokens': 347}}, id='lc_run--019fbc46-6184-7310-b073-a97770ae3309-0', tool_calls=[], invalid_tool_calls=[])]}
"""


history = agent.get_state_history(config)
for snapshot in history:
    print("=" * 50)
    print("Checkpoint ID：", snapshot.config)
    print("当前状态：", snapshot.values)
    print("下一个节点：", snapshot.next)
"""
==================================================
Checkpoint ID： {'configurable': {'thread_id': 'session_1', 'checkpoint_ns': '', 'checkpoint_id': '1f18d7e8-9d8c-6a1a-8001-ae453350c91e'}}
当前状态： {'messages': [HumanMessage(content='你好，我是阿苑', additional_kwargs={}, response_metadata={}), AIMessage(content='你好，阿苑！有什么我可以帮你的吗？', additional_kwargs={}, response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'stop', 'request_id': '2e17d1c5-7f71-9114-b607-90b4cf1cbfc5', 'token_usage': {'input_tokens': 336, 'output_tokens': 11, 'prompt_tokens_details': {'cached_tokens': 0}, 'total_tokens': 347}}, id='lc_run--019fbc53-4c7e-71f2-b415-98d55d6d7a77-0', tool_calls=[], invalid_tool_calls=[])]}
下一个节点： ()

==================================================
Checkpoint ID： {'configurable': {'thread_id': 'session_1', 'checkpoint_ns': '', 'checkpoint_id': '1f18d7e8-95d2-6d1a-8000-5c4408b20cf6'}}
当前状态： {'messages': [HumanMessage(content='你好，我是阿苑', additional_kwargs={}, response_metadata={})]}
下一个节点： ('llm_call',)

==================================================
Checkpoint ID： {'configurable': {'thread_id': 'session_1', 'checkpoint_ns': '', 'checkpoint_id': '1f18d7e8-95cf-69a3-bfff-c098cc10099b'}}
当前状态： {'messages': []}
下一个节点： ('__start__',)
"""






# config = {
#     "configurable": {
#         "thread_id": "session_2"
#     }
# }
# result = agent.invoke({
#     "messages": [HumanMessage(content='你好，我是谁?')],
#     },
#     config=config
# )
# print("助手:", result['messages'][-1].content)
# state_snapshot = agent.get_state(config)
# print(f"备份2：{state_snapshot.values}")
"""
备份2：{'messages': [HumanMessage(content='你好，我是阿苑', additional_kwargs={}, response_metadata={}), 
AIMessage(content='你好，阿苑！有什么我可以帮你的吗？', ad-max', 'finish_reason': 'stop', 'request_id': '-a0ae-c96e7]), 
HumanMessage(content='你好，我是谁?', additional_kwargs={}, response_metadata={}), 
AIMessage(content='你是阿苑！', additional_kwargls=[], invalid_tool_calls=[])]}
"""