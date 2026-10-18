from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# question 1
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role":"user", "content": "你好，我是John,是一个AI老师"}
    ]
)

print(completion.choices[0].message.content)

# question 2
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role":"user", "content": "我是谁"}
    ]
)

print(completion.choices[0].message.content)
