from typing import Dict

_facts_store: Dict[str, Dict[str, str]] = {}

class FactsManager:
    def __init__(self, chat_session_id: str) -> None:
        self.chat_session_id = chat_session_id
        if self.chat_session_id not in _facts_store:
            _facts_store[self.chat_session_id] = {}
    def get_all_facts(self) -> Dict[str, str]:
        return _facts_store.get(self.chat_session_id, {}).copy()

    def get_fact(self, key:str) -> str:
        return _facts_store.get(self.chat_session_id, {}).get(key, "")

    def update_fact(self, facts:Dict[str,str]) -> None:
        if self.chat_session_id not in _facts_store:
            _facts_store[self.chat_session_id] = {}
        _facts_store.get(self.chat_session_id).update({
            k: v for k, v in facts.items() if v
        })

    def set_fact(self, key: str, value: str) -> None:
        if self.chat_session_id not in _facts_store:
            _facts_store[self.chat_session_id] = {}
        if value:
            _facts_store[self.chat_session_id][key] = value

    def clear_facts(self) -> None:
        if self.chat_session_id in _facts_store:
            _facts_store[self.chat_session_id] = {}

    def delete_session(self) -> None:
        if self.chat_session_id in _facts_store:
            del _facts_store[self.chat_session_id]