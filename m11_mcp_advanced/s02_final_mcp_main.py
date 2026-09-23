import json
import os
import asyncio
from urllib.parse import urlsplit

# --- 核心：导入官方库 ---
from langchain_mcp_adapters.client import MultiServerMCPClient

# LangChain/LangGraph 组件
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# 复用你的流式输出模块和配置
from m11_mcp_advanced.s01_agent_stream import run_agent_with_streaming
from config import OPENAI_API_KEY, AMAP_MAPS_API_KEY


def required_env(name: str) -> str:
    """避免在可选远端 MCP 配置中发送空 URL 或空 Bearer 凭据。"""
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"请先设置非空的 {name}")
    return value


def required_mcp_url(name: str) -> str:
    """远端 Bearer 凭据仅发往 HTTPS；本机回环地址可用于离线练习。"""
    value = required_env(name)
    parsed = urlsplit(value)
    loopback_http = parsed.scheme == "http" and parsed.hostname in {
        "localhost", "127.0.0.1", "::1"
    }
    if not parsed.hostname or (parsed.scheme != "https" and not loopback_http):
        raise ValueError(f"{name} 必须是 HTTPS，或本机回环测试地址")
    return value


# === 配置 MCP 服务器 ===
MCP_SERVERS = {
    # 方式1.1: 云端代理 —— stdio模式
    "高德地图": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "@amap/amap-maps-mcp-server"],
        "env": {**os.environ, "AMAP_MAPS_API_KEY": AMAP_MAPS_API_KEY}
    },

    # 方式1.2: 云端MCP服务 —— Streamable HTTP模式
    # "高德地图" :{
    #     "transport":"streamable_http",
    #     "url": f"https://mcp.amap.com/mcp?key={AMAP_MAPS_API_KEY}"
    # },

    # 方式1.3: 需要 Bearer Header 的远端 MCP（可选）
    # 在根目录 .env 中设置 MCP_HTTP_URL 和 MCP_BEARER_TOKEN 后再取消注释。
    # 如果只测试这个服务，也请注释上方默认启用的高德 stdio 配置。
    # "远端 Bearer MCP": {
    #     "transport": "streamable_http",
    #     "url": required_mcp_url("MCP_HTTP_URL"),
    #     "headers": {
    #         "Authorization": f"Bearer {required_env('MCP_BEARER_TOKEN')}"
    #     },
    # },

    # 方式2.1: 本地工具 —— stdio模式
    # "本地天气":{
    #     "transport": "stdio",
    #     "command": "python",
    #     "args": ["-m", "m10_mcp_basics.s01_stdio_server"],
    #     "env": None
    # },

    # 方式2.2:本地MCP服务 —— Streamable HTTP 模式
    # 注:此方法需要提前运行m10的 s02_streamable_http_server.py
    # "本地天气":{
    #     "transport":"streamable_http",
    #     "url": "http://127.0.0.1:8001/mcp"
    # }
}


def build_graph(available_tools):
    """构建图逻辑 (保持不变)"""
    if not available_tools:
        print("⚠️ 未加载任何工具")

    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com",
        streaming=True
    )

    llm_with_tools = llm.bind_tools(available_tools) if available_tools else llm

    sys_prompt = "你是一个地理位置助手，请根据用户需求调用工具查询信息。"

    async def agent_node(state: MessagesState):
        # 格式化消息，确保ToolMessage的content是字符串
        formatted_messages = []
        for msg in state["messages"]:
            if isinstance(msg,ToolMessage) and not isinstance(msg.content,str):
                # 将list/dict转为JSON字符串
                formatted_messages.append(
                    ToolMessage(
                        content=json.dumps(msg.content,ensure_ascii=False),
                        tool_call_id=msg.tool_call_id
                    )
                )
            else:
                formatted_messages.append(msg)
        messages = [SystemMessage(content=sys_prompt)] + formatted_messages
        return {"messages": [await llm_with_tools.ainvoke(messages)]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", agent_node)

    if available_tools:
        workflow.add_node("tools", ToolNode(available_tools))

        def should_continue(state):
            last_msg = state["messages"][-1]
            return "tools" if last_msg.tool_calls else END

        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")
    else:
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

    return workflow.compile()


async def main():
    print("🔌 正在初始化 MCP 客户端...")

    client = MultiServerMCPClient(MCP_SERVERS)

    # 显式建立连接并获取工具
    # 注意：这个 client 对象会保持连接，直到脚本结束
    tools = await client.get_tools()
    print(f"✅ 成功加载工具: {[t.name for t in tools]}")

    # 构建并运行
    app = build_graph(tools)
    query = "帮我查一下杭州西湖附近的酒店"
    await run_agent_with_streaming(app, query)


if __name__ == "__main__":
    asyncio.run(main())
