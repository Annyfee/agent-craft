"""通过官方 MCP 适配器直接练习免费、无需 Key 的网页搜索和抓取。"""

import argparse
import asyncio
import json
import uuid

from langchain_mcp_adapters.client import MultiServerMCPClient


MCP_SERVERS = {
    "parallel": {
        "transport": "streamable_http",
        "url": "https://search.parallel.ai/mcp",
        "headers": {
            "User-Agent": "agent-craft/0.1 (Parallel Search MCP example)"
        },
        "timeout": 60,
    }
}


async def run_tool(name: str, arguments: dict):
    """从服务器发现工具，再通过 LangChain 工具接口调用。"""
    client = MultiServerMCPClient(MCP_SERVERS)
    tools = await client.get_tools()
    tool = next((tool for tool in tools if tool.name == name), None)
    if tool is None:
        raise RuntimeError(f"服务器未提供工具：{name}")
    return await tool.ainvoke(arguments)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    search = commands.add_parser("search", help="搜索网页")
    search.add_argument("objective", help="希望找到的信息")
    search.add_argument("--query", action="append", required=True,
                        help="关键词查询，可重复传入")
    fetch = commands.add_parser("fetch", help="抓取指定网页的内容摘要")
    fetch.add_argument("urls", nargs="+", help="网页的 HTTP/HTTPS URL")
    args = parser.parse_args()

    # 一次命令对应一次独立查询，不读取 .env 或任何服务密钥。
    arguments = {"session_id": str(uuid.uuid4())}
    if args.command == "search":
        name = "web_search"
        arguments.update(objective=args.objective, search_queries=args.query)
    else:
        name = "web_fetch"
        arguments.update(urls=args.urls)
    result = asyncio.run(run_tool(name, arguments))
    # 保留适配器返回的内容块（包括来源），而不是只取第一个文本块。
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
