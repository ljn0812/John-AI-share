from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

chat_history = []

# question 1
user_message_1 = "你好，我是John,是一个AI老师"

chat_history.append({"role":"user", "content": user_message_1})

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=chat_history
)

print(completion.choices[0].message.content)

ai_reply_1 = completion.choices[0].message.content

chat_history.append({"role":"assistant", "content": ai_reply_1})


# question 2 with chat history
user_message_2="我是谁"

chat_history.append({"role":"user", "content": user_message_2})
print(chat_history)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=chat_history
)

print(completion.choices[0].message.content)