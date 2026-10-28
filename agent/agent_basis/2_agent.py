from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


@tool
def good_search(id:str) ->str:
    """
    A tool to search for good items by ID.
    :param id: The ID of the item to search for.
    :return: The search results.
    """
    good_list = {
        "1": "Good item 1 details",
        "2": "Good item 2 details",
        "3": "Good item 3 details"
    }
    print(f"Searching for good item with ID: {id}")
    return good_list[id]


agent = create_agent(
    model=ChatTongyi(model="qwen3.7-max"),
    tools=[good_search],
    system_prompt="You are a helpful assistant that can search for good items by ID."
)

user_input = "请帮我查找ID为2的商品信息。"
result = agent.invoke(
    {"messages":[{"role":"user","content": user_input}]}
)

print(result['messages'][-1].content)  # 输出最后一条消息的内容