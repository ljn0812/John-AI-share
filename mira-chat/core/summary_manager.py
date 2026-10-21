from typing import Dict, List

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.prompt import SUMMARY_GENERATION_PROMPT

_summary_store: Dict[str, str] = {}

_unsummarized_count: Dict[str, int] = {} 

SUMMARY_BATCH_SIZE = 12

str_output_parser = StrOutputParser()

class SummaryManager:
    def __init__(self, chat_session_id: str) -> None:
        self.chat_session_id = chat_session_id
        if chat_session_id not in _summary_store:
            _summary_store[chat_session_id] = ""
        if chat_session_id not in _unsummarized_count:
            _unsummarized_count[chat_session_id] = 0

    def get_summary(self) -> str:
        return _summary_store.get(self.chat_session_id, "")

    def update_summary(self, new_summary: str) -> None:
        _summary_store[self.chat_session_id] = new_summary

    def get_unsummarized_count(self) -> int:
        return _unsummarized_count.get(self.chat_session_id, 0)

    def increment_unsummarized_count(self, delta: int = 1) -> None:
        current = _unsummarized_count.get(self.chat_session_id, 0)
        _unsummarized_count[self.chat_session_id] = current + delta

    def reset_unsummarized_count(self) -> None:
        _unsummarized_count[self.chat_session_id] = 0

    def should_trigger_summary(self) -> bool:
        return self.get_unsummarized_count() >= SUMMARY_BATCH_SIZE

    def generate_incremental_summary(self, old_summary: str,new_messages:List[BaseMessage],llm: ChatTongyi|None) -> str:
        if not new_messages:
            return old_summary

        message_text = ""
        for msg in new_messages:
            if isinstance(msg, HumanMessage):
                message_text += f"human: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                message_text += f"ai: {msg.content}\n"

        if not llm:
            return self._simple_summary(old_summary,message_text)

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system",SUMMARY_GENERATION_PROMPT),
                ("human",f"旧摘要: {old_summary}\n新摘要: {message_text}")
            ])

            chain = prompt | llm | str_output_parser
            result = chain.invoke(input={})
            new_summary = result.strip()
            return new_summary

        except:
            return self._simple_summary(old_summary, message_text)





    def _simple_summary(self, old_summary: str, messages_text: str):
        if old_summary and old_summary != "[摘要] 无":
            old_part = old_summary[:150] if len(old_summary) >= 150 else old_summary
            new_part = messages_text[:150] if len(messages_text) >= 150 else messages_text
            return f"[摘要] {old_part}...{new_part}"
        else:
            new_part = messages_text[:150] if len(messages_text) >= 150 else messages_text
            return f"[摘要] {new_part}"
