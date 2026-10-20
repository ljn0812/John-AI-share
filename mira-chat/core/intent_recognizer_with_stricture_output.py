import json
import re
from typing import Any

from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from core.prompt import INTENT_RECOGNIZE_PROMPT, INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT


class IntentResult(BaseModel):
    intents: list[str] = Field(...,description="意图列表，每一个元素为一个意图名称")
    slots: dict[str, Any] = Field(...,description="slot字典，键为slot名称，值为slot值")
    confidence: float = Field(...,description="置信度分数，取值范围0-1，越大表示越确信该意图")


class IntentRecognizer:
    def __init__(self, llm: ChatTongyi):
        self.__llm = llm.with_structured_output(IntentResult)
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system",INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT),
            ("ai","上下文内容: {chat_history}"),
            ("human","用户输入: {user_input}")
        ])
        self.__chain = self.__prompt | self.__llm

    def recognize(self, user_input: str, chat_history: str | None=None) -> IntentResult:
        chat_history = chat_history if chat_history else ""
        result = self.__chain.invoke(input={"chat_history": chat_history, "user_input": user_input})

        if result is None:
            return IntentResult(intents=["general"], slots={}, confidence=0.0)

        return result

