import os
from openai import OpenAI

# creat the model client
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# call the model
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
    stream=True,
    stream_options={"include_usage": True},
)

# output print
for chunk in completion:
    if chunk.choices:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content,end="",flush=True)

