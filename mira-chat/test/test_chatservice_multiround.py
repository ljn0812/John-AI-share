import os


from chat_service import ChatService
from core.protocol import ChatRequest
import uuid

chat_service = ChatService()

session_id = "test_session"
user_id = "test_user"

conversations = [
    "我的订单什么时候发货？",
    "ORD123456789",
    "能改地址吗？",
    "北京市朝阳区xxx",
    "谢谢",
    "没有了",
    "拜拜"
]

for round_num, user_input in enumerate(conversations, 1):
    request = ChatRequest(
        user_id=user_id,
        chat_session_id=session_id,
        trace_id=str(uuid.uuid4()),
        user_input=user_input,
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )

    print(f"第{round_num}轮 - 用户: {user_input}")
    result = chat_service.handle(request)
    print(f"AI: {result.response}\n")