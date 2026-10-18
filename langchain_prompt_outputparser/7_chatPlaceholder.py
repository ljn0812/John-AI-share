from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat = ChatPromptTemplate.from_messages([
    ("system","假设你是一个AI专家"),
    MessagesPlaceholder("history"),
    ("human","我刚才问了什么")
])

chat_history = [
    ("human", "什么是Langgraph"),
    ("ai", "LangGraph是一种将自然语言处理（NLP）与图神经网络（GNN, Graph Neural Networks）相结合的技术或方法。")
]

# result = chat.format(history=chat_history)
# print(result)
llm = Tongyi(model="qwen-max",streaming=True)

chain = chat | llm
result = chain.stream({"history":chat_history})
for item in result:
    print(item,end="",flush=True)
