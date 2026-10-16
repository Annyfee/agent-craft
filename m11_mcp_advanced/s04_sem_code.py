"""通过 Streamable HTTP 查询本地代码实体；不需要模型 API Key。"""
import argparse
import asyncio
import json
import os

from langchain_mcp_adapters.client import MultiServerMCPClient


async def lookup(query: str, token: str):
    client = MultiServerMCPClient({
        "sem": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8765/mcp",
            "headers": {"Authorization": f"Bearer {token}"},
            "timeout": 60,
        }
    })
    tools = await client.get_tools()
    tool = next((tool for tool in tools if tool.name == "sem_find"), None)
    if tool is None:
        raise RuntimeError("服务器未提供 sem_find")
    return await tool.ainvoke({"query": query, "mode": "context", "token_budget": 1200})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="代码实体名称，例如 parse_config")
    args = parser.parse_args()
    token = os.environ.get("SEM_MCP_HTTP_TOKEN")
    if not token:
        parser.error("请设置本地 Sem 服务使用的 SEM_MCP_HTTP_TOKEN")
    print(json.dumps(asyncio.run(lookup(args.query, token)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
