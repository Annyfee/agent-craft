from mcp.server.fastmcp import FastMCP

# 初始化服务
# WeatherService 是服务的名字
mcp = FastMCP("WeatherService")

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
    # 默认运行方式:Stdio(标准输入输出)
    # 这种模式下，程序启动后会“挂起”等待指令，不会有任何打印输出。
    mcp.run()