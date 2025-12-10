from typing import Protocol,List,Dict,Any

class MCPTransport(Protocol):
    """MCP 传输层协议 —— 所有 transport必须实现如下方法"""

    async def connect(self):
        """建立连接"""
        ...

    async def list_tools(self):
        """获取工具列表"""
        ...

    async def call_tool(self,name:str,args:dict):
        """调用工具并返回文本结果"""
        ...

    async def cleanup(self):
        """清理资源"""
        ...