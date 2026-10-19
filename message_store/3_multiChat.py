
from typing import Dict, List

from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

_session_store: Dict[str, BaseChatMessageHistory] = {}

class Memory:
    def get_session_history(self, chat_session_id) -> BaseChatMessageHistory:
        if chat_session_id not in _session_store:
            _session_store[chat_session_id] = InMemoryChatMessageHistory()
        return _session_store[chat_session_id]

    def add_human_message(self, chat_session_id: str, message: str | HumanMessage) -> None:
        historty = self.get_session_history(chat_session_id)
        if isinstance(message, str):
            historty.add_message(HumanMessage(message))
        else:
            historty.add_message(message)

    def add_ai_message(self, chat_session_id: str, message: str | AIMessage) -> None:
        historty = self.get_session_history(chat_session_id)
        if isinstance(message, str):
            historty.add_message(AIMessage(message))
        else:
            historty.add_message(message)
    def messages(self, chat_session_id: str) -> List[BaseMessage]:
        return self.get_session_history(chat_session_id).messages

class ChatSession:
    def __init__(self, chat_session_id: str, system_prompt:str = "你是一个友好的AI助手") -> None:
        self.chat_session_id = chat_session_id
        self.memory = Memory()
        self.prompt = ChatPromptTemplate.from_messages([
            "system",system_prompt,
            MessagesPlaceholder("history"),
            ("human","{input}")
        ])
        self.model = ChatTongyi(model="qwen3.7-max", streaming=True)
        self.parser = StrOutputParser()
        self.chain = self.prompt | self.model | self.parser

    def send(self, user_input: str):
        chat_history = self.memory.get_session_history(self.chat_session_id)
        stream = self.chain.stream(input={
                "history": chat_history.messages,
                "input": user_input
        })

        full_reply = ""
        for chunk in stream:
            full_reply += chunk
            yield chunk
        self.memory.add_human_message(self.chat_session_id, user_input)
        self.memory.add_ai_message(self.chat_session_id, full_reply)

if __name__ == "__main__":
    session = ChatSession("user001")

    print("用户：你好，我是John")
    print("AI:",end="",flush=True)
    for chunk in session.send("你好，我叫John"):
        print(chunk,end="",flush=True)
    print()

    print("用户：我叫什么名字？")
    print("AI:",end="",flush=True)
    for chunk in session.send("我叫什么名字"):
        print(chunk,end="",flush=True)
    print()