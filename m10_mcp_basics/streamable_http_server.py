from mcp.server.fastmcp import FastMCP


# 创建服务实例，指定监听地址和端口
mcp = FastMCP("WeatherService",host="0.0.0.0",port=8001)

# 业务逻辑工具
@mcp.tool()
async def get_weather(city:str):
    """
    查询指定城市的实时天气。
    如果是此时此刻的天气请求，调用此工具。
    """
    # 模拟真实的网络请求(你可以换成自己的天气API)
    # 在MCP中，工具函数可以是async的，FastMCP会自动处理
    return f"{city}的天气是:晴，气温25℃，风力3级"


# 启动入口
if __name__ == '__main__':
    # 运行方式:Streamable HTTP
    # 这会自动启动 uvicorn 服务器，支持远程调用
    mcp.run("streamable-http")