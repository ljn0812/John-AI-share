from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

memory = FileChatMessageHistory("content.text")

memory.add_message(HumanMessage("你是谁"))
memory.add_message(AIMessage("我是AI"))

print(memory)