from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage

chatModel = ChatTongyi(model="qwen3.7-max")

chat_history = [
    SystemMessage(content="背景设定： 你现在是一名AI老师，负责上AI课程"),
    HumanMessage(content="你是谁")
]

reply= chatModel.invoke(input=chat_history)
print(reply.content)


