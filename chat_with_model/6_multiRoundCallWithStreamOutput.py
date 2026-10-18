from openai import OpenAI


class MultiRoundChat:
    def __init__(self, base_url: str, model: str, system_prompt: str=None):
        self.client = OpenAI(base_url=base_url)
        self.model = model
        self.chat_history = []

        if system_prompt:
            self.chat_history.append({"role":"system", "content":system_prompt})

    def send(self, user_message: str):
        self.add_user_message(user_message)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            stream=True,
            stream_options={"include_usage": True}
        )
        reply=""
        for chunk in stream:
            if chunk.choices:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    reply += content
                    yield content
        self.add_assistant_message(reply)

    def add_user_message(self, user_message: str) -> None:
        self.chat_history.append({"role":"user", "content":user_message})

    def add_assistant_message(self, assistant_message: str) -> None:
        self.chat_history.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    MODEL = "qwen3.8-max"
    SYSTEM_MESSAGE = "背景设定： 你现在是一名AI老师，负责上AI课程"
    chat = MultiRoundChat(
        base_url=BASE_URL,
        model=MODEL,
        system_prompt=SYSTEM_MESSAGE
    )

    print("多轮对话已启动，输入内容后按回车发送。输入'exit'或'quit'推出程序。\n")

    while True:
        user_input = input("用户:")

        if user_input in ["exit", "quit"]:
            print("对话结束")
            break
        if not user_input.strip():
            print("请勿输入空白字符")
            continue
        print("AI老师:", end="", flush=True)
        for chunk in chat.send(user_input):
            print(chunk, end="", flush=True)
        print()

