import os
from openai import OpenAI

# creat the model client
client = OpenAI(
    api_key="sk-ws-H.PYILXYE.JlAf.MEYCIQDz4NzjA0MVuel6UCtZqnPWXgvfqNn4SZ492V50YSXVrQIhAItuTEm5wDafIFhT_nyClGEgZJDnhAvTRVkifD0CDHey",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# call the model
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "1+1等于几？"},
    ]
)

# output print
print(completion.model_dump_json())

print(completion.choices[0].message.content)