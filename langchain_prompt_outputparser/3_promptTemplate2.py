from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

llm = Tongyi(model="qwen-max")


pt = PromptTemplate.from_template(
    "假设你是一个{expert}专家，请你解释一下{content}是什么。"
)

prompt = pt.format(expert="AI", content="Langgraph")


result = llm.stream(input=prompt)


for chunk in result:
    print(chunk, end='', flush=True)