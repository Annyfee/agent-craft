import uuid
from contextlib import AsyncExitStack
from typing import Optional,Literal

from .transports.base import MCPTransport
from .transports.http import HttpMCPTransport
from .transports.stdio import StdioMCPTransport


class MCPClient:

    # 编辑器 _impl 必须满足MCPTransport协议
    _impl:MCPTransport

    def __init__(
            self,
            transport:Literal["stdio","http"]="stdio",
            command:str=None,
            args:list[str]=None,
            env:dict=None,
            url:str=None
    ):
        """
        MCP 客户端 - 支持 stdio 与 HTTP 两种传输方式

        :param transport: 传输模式 "stdio" / "http"
        :param command: stdio 模式的命令 （如npx）
        :param args: stdio 模式的参数
        :param env: stdio 模式的环境变量
        :param url: http模式的端点 URL
        """

        if transport=="stdio":
            if command is None:
                raise ValueError("stdio 传输模式需要参数 'command'")
            self._impl = StdioMCPTransport(command=command,args=args or [],env=env)
        elif transport=="http":
            if url is None:
                raise ValueError("http 传输模式需要参数 'command'")
            self._impl = HttpMCPTransport(url=url)
        else:
            raise ValueError(f"不支持的传输模式: {transport}")



    async def connect(self):
        """ 建立MCP连接(stdio或HTTP) """
        await self._impl.connect()


    async def list_tools(self):
        """查询工具列表，为LLM建立上下文用"""
        return await self._impl.list_tools()

    async def call_tool(self,name:str,args:dict):
        """调用工具（工程化：加上防御性处理）"""
        return await self._impl.call_tool(name,args)


    async def cleanup(self):
        """关闭MCP服务、会话和transport"""
        return await self._impl.cleanup()


    async def _http_request(self,method:str,params:dict=None):
        """ 发送 HTTP JSON-RPC 请求 """
        payload = {
            "jsonrpc":"2.0",
            "id":str(uuid.uuid4()),
            "method":method,
        }
        if params:
            payload["params"] = params

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        response = await self.http_client.post(
            self.url,
            json=payload,
            headers=headers
        )

        if "Mcp-Session-Id" in response.headers:
            self.session_id = response.headers["Mcp-Session-Id"]

        response.raise_for_status()
        return response.json()