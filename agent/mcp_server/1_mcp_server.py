
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="weather")

@mcp.tool()
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    return f"{location}的天气情况是70摄氏度。请你不要出门"



if __name__ == '__main__':

    print("启动 MCP 服务，监听 stdio 传输...")
    mcp.run(transport="stdio") 