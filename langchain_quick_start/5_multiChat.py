from langchain_community.chat_models import ChatTongyi


class MultiChat:
    def __init__(self, model: str, system_prompt: str = None) -> None:
        self.llm = ChatTongyi(model=model, streaming=True)
        self.chat_history = []
        if system_prompt:
            self.chat_history.append(('system', system_prompt))

    def send(self, user_message: str):

        self.add_user_message(user_message)

        stream = self.llm.stream(input=self.chat_history)
        full_reply = ""
        for chunk in stream:
            if chunk.content:
                full_reply += chunk.content
                yield chunk.content
        self.add_ai_message(full_reply)

    def add_user_message(self, user_message: str):
        self.chat_history.append(('human', user_message))

    def add_ai_message(self, ai_message: str):
        self.chat_history.append(('ai', ai_message))

if __name__ == "__main__":

    MODEL="qwen3.7-max"
    SYSTEM_PROMPT = "背景设定： 你现在是一名AI老师，负责上AI课程"

    chat = MultiChat(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
    )

    print("多轮对话已启动，输入内容后按回车发送。输入'exit'或'quit'推出程序。\n")

    while True:
        user_input = input("用户:")
        if user_input in ('exit', 'quit'):
            print("对话结束")
            break
        if not user_input.strip():
            print("请勿输入空白字符")
            continue
        print("AI:",end="",flush=True)
        for chunk in chat.send(user_input):
            print(chunk,end="",flush=True)
        print()
