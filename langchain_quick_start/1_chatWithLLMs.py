from langchain_community.llms.tongyi import Tongyi

llm = Tongyi(model="qwen-max")

reply = llm.invoke(input="你是谁？")

print(type(reply))
print(reply)
