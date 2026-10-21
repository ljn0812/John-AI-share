from typing import List, Dict

from langchain_core import messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from core.chat_history_manager import ChatHistoryManager
from core.facts_manager import FactsManager
from core.summary_manager import SummaryManager

SESSION_KEY = "session"

class Memory:
    def __init__(self, chat_session_id: str) -> None:
        self.chat_session_id = chat_session_id
        self.session_key = f"{SESSION_KEY}:{chat_session_id}"
        self.history = ChatHistoryManager(self.session_key)
        self.summary = SummaryManager(self.session_key)
        self.facts = FactsManager(self.session_key)

    def get_session_history(self):
        return self.history.get_history()

    def get_recent_history(self, recent_n: int) -> List[BaseMessage]:
        return self.history.get_recent_messages(recent_n)

    def get_messages(self) -> List[BaseMessage]:
        return self.history.get_messages()

    def get_recent_history_text(self, recent_n: int) -> str:
        result = self.get_recent_history(recent_n)
        full_text = ""
        for msg in result:
            if isinstance(msg, HumanMessage):
                full_text += f"human: {msg.content}\n"
            if isinstance(msg, AIMessage):
                full_text += f"ai: {msg.content}\n"
        return full_text

    def add_user_message(self, message: str, llm=None) -> None:
        self.history.add_user_message(message)
        self.summary.increment_unsummarized_count(1)
        self._trim_and_summarized(llm)

    def add_ai_message(self, message: str, llm=None) -> None:
        self.history.add_ai_message(message)
        self.summary.increment_unsummarized_count(1)
        self._trim_and_summarized(llm)

    def get_key_facts(self) -> Dict[str, str]:
        return self.facts.get_all_facts()

    def update_key_facts(self, new_facts: Dict[str, str]) -> None:
        self.facts.update_fact(new_facts)

    def clear_facts(self) -> None:
        self.facts.clear_facts()


    def _trim_and_summarized(self, llm=None):
        if not self.summary.should_trigger_summary():
            return
        history = self.get_session_history()
        if not history:
            return

        messages = self.get_messages()
        unsummarized_count = self.summary.get_unsummarized_count()
        summarized_count = len(messages) - unsummarized_count
        new_messages = messages[summarized_count:]
        if new_messages:
            old_summary = self.summary.get_summary()
            new_summary = self.summary.generate_incremental_summary(old_summary,new_messages,llm)
            self.summary.update_summary(new_summary)
            self.summary.reset_unsummarized_count()
            print("摘要生成")

    def prepare_memory_for_llm(self) -> List[BaseMessage]:
        result = []
        facts = self.facts.get_all_facts()
        if facts:
            facts_text = " | ".join([f"{k}:{v}" for k, v in facts.items()])
            result.append(AIMessage(content=f"[关键事实] {facts_text}"))
        summary = self.summary.get_summary()
        if summary:
            result.append(AIMessage(content=f"[摘要] {summary}"))

        unsummarized_count = self.summary.get_unsummarized_count()
        if unsummarized_count > 0:
            messages = self.history.get_messages()
            recent_messages = messages[-unsummarized_count:]
            result.extend(recent_messages)
        return result