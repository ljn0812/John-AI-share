from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {"input": "高兴", "output": "愉悦"},
    {"input": "快速", "output": "迅猛"},
    {"input": "美丽", "output": "绚丽"}
]

example_prompt = PromptTemplate.from_template(
    template="输入：{input}\n输出：{output}"
)

fewShot = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请根据一下示例，将用户输入的词语转换为同义词",
    suffix="用户输入:{word}\n输出:",
    input_variables=["word"]
)

#
# prompt = fewShot.format(word="悲伤")
#
# print(prompt)

llm = Tongyi(model="qwen-max")

chain = fewShot | llm
stream = chain.stream({"word":"美味"})
for chunk in stream:
    print(chunk, end="", flush=True)