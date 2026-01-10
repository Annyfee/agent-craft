import os
import asyncio

# --- 核心：导入官方库 ---
from langchain_mcp_adapters.client import MultiServerMCPClient

# LangChain/LangGraph 组件
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# 复用你的流式输出模块和配置
from m11_mcp_advanced.s01_agent_stream import run_agent_with_streaming
from config import OPENAI_API_KEY, AMAP_MAPS_API_KEY

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
        messages = [SystemMessage(content=sys_prompt)] + state["messages"]
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