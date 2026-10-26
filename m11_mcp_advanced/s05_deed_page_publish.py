"""通过官方 MCP 适配器练习把本地 HTML 发布成公开网页（deed.page，无需注册或 Key）。"""

import argparse
import asyncio
import json
import os
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient


MCP_SERVERS = {
    "deed_page": {
        "transport": "streamable_http",
        "url": "https://deed.page/mcp",
        "headers": {
            "User-Agent": "agent-craft/0.1 (deed.page MCP example)"
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
    publish = commands.add_parser("publish", help="把一个 HTML 文件发布为 index.html")
    publish.add_argument("file", type=Path, help="本地 HTML 文件")
    publish.add_argument("--slug", help="网址前缀，省略则随机生成")
    publish.add_argument("--ttl", type=int, help="可选：多少秒后自动过期，省略则长期保留")
    get = commands.add_parser("get", help="查询某个 slug 是否在线（无需 token）")
    get.add_argument("slug")
    delete = commands.add_parser("delete", help="删除自己发布的页面")
    delete.add_argument("slug")
    args = parser.parse_args()

    # 不读取 .env；只有删除时需要首次发布返回的 token，从环境变量传入，避免写进命令历史。
    if args.command == "publish":
        name = "publish_site"
        arguments = {"files": {"index.html": args.file.read_text(encoding="utf-8")}}
        if args.slug:
            arguments["slug"] = args.slug
        if args.ttl:
            arguments["ttl_seconds"] = args.ttl
    elif args.command == "get":
        name, arguments = "get_site", {"slug": args.slug}
    else:
        token = os.environ.get("DEED_PAGE_TOKEN", "").strip()
        if not token:
            parser.error("delete 需要环境变量 DEED_PAGE_TOKEN（首次发布结果中的 token）")
        name, arguments = "delete_site", {"slug": args.slug, "token": token}
    result = asyncio.run(run_tool(name, arguments))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
