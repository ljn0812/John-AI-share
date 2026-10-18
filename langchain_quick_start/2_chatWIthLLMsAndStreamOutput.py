from langchain_community.llms.tongyi import Tongyi

llm = Tongyi(model="qwen-max")

reply = llm.stream(input="你是谁？")

for chunk in reply:
    print(chunk, end="", flush=True)
