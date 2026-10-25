from typing import List

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate

from querying.query_prompt import REWRITE_PROMPT


class QueryRewriter:

    REFERENCE_KEYWORDS = ["那篇", "刚才", "它", "这个", "该", "那", "这", "其"]

    def __init__(self, llm: ChatTongyi):
        self._llm = llm
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", REWRITE_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "用户问题：{question}\n改写后的查询：")
        ])
        self.chain = self._prompt | self._llm | StrOutputParser()


    def rewrite(self, question: str, chat_history: List[BaseMessage]) -> str:

        if not question:
            return question

        if not self._needs_rewrite(question):
            return question
        try:
            chat_history = chat_history or []

            result = self.chain.invoke({
                "question": question,
                "chat_history": chat_history
            })
            return result
        except Exception as e:
            print(f"Error occurred while rewriting query: {e}")
            return question

    def _needs_rewrite(self, query: str) -> bool:
        return any(keyword in query for keyword in self.REFERENCE_KEYWORDS)