import asyncio

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_mcp_adapters.client import MultiServerMCPClient



async def main():
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": "python",
                "args": ["D:\\PythonProject\\John-AI-share\\agent\\mcp_server\\weather.py"]
            }
        }
    )

    tool = await client.get_tools()

    agent = create_agent(
        model = ChatTongyi(model="qwen3.7-max"),
        tools = tool,
        system_prompt = "你是一个天气查询助手。"
    )

    result = await agent.ainvoke(
        {"messages": [{"role":"user", "content" : "北京的天气情况怎么样?"}]}
    )

    print(result)
    print(result["messages"][-1].content)

if __name__ == '__main__':
    asyncio.run(main())