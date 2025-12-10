import json
import uuid
from typing import Optional,Literal

import httpx


class HttpMCPTransport:
    def __init__(self,url:str=None):
        """
        MCP 客户端 - 支持 stdio 与 HTTP 两种传输方式

        :param url: http模式的端点 URL
        """
        if not url:
            raise ValueError("HTTP模式必须提供url参数")
        self.url = url
        self.session_id:Optional[str] = None
        self.http_client:Optional[httpx.AsyncClient] = None



    async def connect(self):
        """建立MCP长连接（一次连接，多次调用）"""
        if self.http_client:
            return
        self.http_client = httpx.AsyncClient(timeout=60.0)

        # 发送 initialize 请求
        response = await self._http_request("initialize",{
            "protocolVersion":"2024-11-05",
            "capabilities":{},
            "clientInfo":{"name":"mcp-client","version":"1.0"}
        })

        # 保存session ID
        if response and "result" in response:
            # Session ID在响应头内
            pass # 已在_http_request中处理


    async def list_tools(self):
        """查询工具列表，为LLM建立上下文用"""
        if not self.http_client:
            raise RuntimeError("未连接，请先 connect()")

        result = await self._http_request("tools/list")
        if result and "result" in result:
            tools = result["result"].get("tools",[])
            return [
                {
                    "name":tool["name"],
                    "description":tool["description"],
                    "input_schema":tool.get("inputSchema",{})
                }
                for tool in tools
            ]
        return []


    async def call_tool(self,name:str,args:dict):
        """调用工具（工程化：加上防御性处理）"""
        if not self.http_client:
            raise RuntimeError("未连接，请先 connect()")

        result = await self._http_request("tools/call",{
            "name":name,
            "arguments":args
        })
        if result and "result" in result:
            content = result["result"].get("content",{})
            if content and len(content):
                return content[0].get("text",str(content[0]))

        return "工具执行成功，但无文本返回"


    async def cleanup(self):
        """关闭MCP服务、会话和transport"""
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None
            self.session_id = None


    async def _http_request(self, method: str, params: dict = None):
        """ 发送 HTTP JSON-RPC 请求 """
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
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

        # 判断响应类型
        content_type = response.headers.get("Content-Type", "")

        if "text/event-stream" in content_type:
            # SSE 流式响应（本地服务器）
            for line in response.text.split('\n'):
                line = line.strip()
                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    try:
                        return json.loads(data_str)
                    except json.JSONDecodeError:
                        pass
            return None
        else:
            # 普通 JSON 响应（云端服务）
            return response.json()
