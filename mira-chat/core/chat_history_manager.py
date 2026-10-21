from typing import Dict, List
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage

_session_store: Dict[str, BaseChatMessageHistory] = {}

class ChatHistoryManager:

    def __init__(self, chat_session_id: str) -> None:
        self.chat_session_id = chat_session_id

    def get_history(self) -> BaseChatMessageHistory:
        if self.chat_session_id not in _session_store:
            _session_store[self.chat_session_id] = InMemoryChatMessageHistory()
        return _session_store[self.chat_session_id]

    def get_messages(self) -> List[BaseMessage]:
        return self.get_history().messages

    def add_user_message(self, content: str) -> None:
        self.get_history().add_user_message(content)

    def add_ai_message(self, content: str) -> None:
        self.get_history().add_ai_message(content)

    def get_recent_messages(self, count: int) -> List[BaseMessage]:
        messages = self.get_messages()
        return messages[-count:] if messages else []

    def clear(self) -> None:
        if self.chat_session_id in _session_store:
            _session_store[self.chat_session_id] = InMemoryChatMessageHistory()