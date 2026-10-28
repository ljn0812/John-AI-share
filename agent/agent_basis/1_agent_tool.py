from langchain_community.chat_models import ChatTongyi
from langchain.tools import tool
from langchain.messages import ToolMessage

llm = ChatTongyi(model="qwen3.7-max")



@tool
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """

    return f"{location}的天气情况是70摄氏度。请你不要出门"


tools = [get_weather]
llm_with_tools = llm.bind_tools(tools=tools)


user_input = "北京的天气情况怎么样?"
messages = [
    ("system", "你是一个天气查询助手。"),
    ("human", f"{user_input}")
]

result = llm_with_tools.invoke(messages)

tool_map = {tool.name: tool for tool in tools}

if result.tool_calls:
    messages.append(result)

    for tool_call in result.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        tool_func = tool_map.get(tool_name)

        if tool_func:
            try:
                tool_result = tool_func.invoke(tool_args)
                print(f"Tool '{tool_name}' executed successfully. Result: {tool_result}")

                tool_message = ToolMessage(
                    content = tool_result,
                    tool_call_id = tool_id
                )
                messages.append(tool_message)

            except Exception as e:
                tool_message = ToolMessage(
                    content=f"工具调用失败: {str(e)}",
                    tool_call_id=tool_id
                )
                messages.append(tool_message)
        else:
            print(f"未找到工具：{tool_name}")
            tool_message = ToolMessage(
                content=f"未找到工具: {tool_name}",
                tool_call_id=tool_id
            )
            messages.append(tool_message)
else:
    print("没有需要调用的工具")
    print(result.content)

result = llm_with_tools.invoke(messages)
print(result.content)