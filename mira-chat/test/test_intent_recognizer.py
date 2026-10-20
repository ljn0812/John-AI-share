from langchain_community.chat_models import ChatTongyi

from core.intent_recognizer import IntentRecognizer

if __name__ == '__main__':
    llm = ChatTongyi(model="qwen3.7-max")
    Recognizer = IntentRecognizer(llm)
    result= Recognizer.recognize("我的订单号是123456789")
    print(result)

    result = Recognizer.recognize("我的订单号是123456789","human:我要退货\nai:请提供你的单号")
    print(result)