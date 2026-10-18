from langchain_community.llms.tongyi import Tongyi


llm = Tongyi(model="qwen-max")


user_query = "假设你是一个{expert}专家，请你解释一下{content}是什么。".format(expert="AI", content="Langgraph")

result = llm.stream(input=user_query)


for chunk in result:
    print(chunk, end='', flush=True)