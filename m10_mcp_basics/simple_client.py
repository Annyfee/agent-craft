from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

class SimpleClient:
    def __init__(self,command:str,args:list[str],env:dict=None):
        # 指定要启动的工具和参数
        self.params = StdioServerParameters(command=command,args=args,env=env)

    async def run_once(self,tool_name:str,tool_args:dict):
        # 语法糖: async with 自动帮我们 打开连接 -> 运行 -> 关闭连接
        async with stdio_client(self.params) as (read,write):
            # 建立父子进程管道（stdin/stdout）
            async with ClientSession(read,write) as session:
            # 用JSON-RPC与工具对话
                await session.initialize()

                # 直接调用工具
                result = await session.call_tool(tool_name,tool_args)
                return result.content[0].text