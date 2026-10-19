from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

memory = InMemoryChatMessageHistory()

memory.add_message(HumanMessage("你是谁"))
memory.add_message(AIMessage("我是AI"))

print(memory.messages)
print(memory)