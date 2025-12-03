from contextlib import AsyncExitStack
from typing import Optional
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self,command:str,args:list[str],env:dict=None):
        # MCP启动方式(npx/uvx/python -m xxx)
        self.params = StdioServerParameters(command=command,args=args,env=env)
        # 工程核心:资源栈
        self.exit_stack = AsyncExitStack()
        # 连接会话(长连接)
        self.session:Optional[ClientSession]=None

    async def connect(self):
        """建立MCP长连接（一次连接，多次调用）"""
        if self.session:
            return # 已连接无需重复

        # 进入transport（读/写管道）
        transport = await self.exit_stack.enter_async_context(
            stdio_client(self.params)
        )
        # 创建JSON-RPC对话
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(transport[0],transport[1])
        )
        # 等待MCP服务器返回工具清单
        await self.session.initialize()

    async def list_tools(self):
        """查询工具列表，为LLM建立上下文用"""
        if not self.session:
            raise RuntimeError("未连接，请先 connect()")

        result = await self.session.list_tools()

        # 🔍 调试：打印工具的完整信息，确认工具是否被正确封装
        # if result.tools:
        #     import json
        #     # 使用 model_dump() (Pydantic v2) 或 dict() (v1) 查看原始数据
        #     first_tool = result.tools[0]
        #     print(f"\n🔍 [DEBUG] 原始工具数据: {first_tool}\n")

        # 转为纯字典,LLM能读
        return[
            {
                "name":tool.name,
                "description":tool.description,
                "input_schema":tool.inputSchema
            }
            for tool in result.tools
        ]

    async def call_tool(self,name:str,args:dict):
        """调用工具（工程化：加上防御性处理）"""
        if not self.session:
            raise RuntimeError("未连接，请先connect()")

        result = await self.session.call_tool(name,args)

        # 有些工具可能执行成功但无文本返回
        if hasattr(result,"content") and result.content:
            return result.content[0].text

        return "工具执行成功，但无文本返回"

    async def cleanup(self):
        """关闭MCP服务、会话和transport"""
        if self.session:
            await self.exit_stack.aclose()
            self.session = None