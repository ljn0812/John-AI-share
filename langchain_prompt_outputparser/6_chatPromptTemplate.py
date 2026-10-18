from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import ChatPromptTemplate

chat = ChatPromptTemplate.from_messages([
    ("system","假设你是一个{expert}专家"),
    ("human","什么是{user_input}")
])

llm = Tongyi(model="qwen-max",streaming=True)

chain = chat | llm


result = chain.stream( {"expert":"AI","user_input":"langchain"})
print(chat)
for item in result:
    print(item,end="",flush=True)
