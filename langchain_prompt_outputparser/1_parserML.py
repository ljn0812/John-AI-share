from langchain_community.llms import Tongyi

llm = Tongyi(model="qwen-max",streaming=True)

user_query1 = "介绍一下机器学习"
user_query_2 = """
                请从以下几个方面介绍机器学习：
                1. 定义（一句话概括）
                2. 三大分类（监督学习、无监督学习、强化学习）
                3. 一个生活化的例子
                4. 与深度学习的区别（用表格呈现）
                
                要求：语言通俗，适合零基础初学者
                """

reply1 = llm.stream(user_query1)
reply2 = llm.stream(user_query_2)

for chunk1 in reply1:
    print(chunk1,end="",flush=True)

for chunk2 in reply2:
    print(chunk2,end="",flush=True)