import os
import sys
from contextlib import AsyncExitStack
import asyncio

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.prebuilt import ToolNode

from config import OPENAI_API_KEY,AMAP_MAPS_API_KEY
from m11_mcp_advanced.s01_agent_stream import run_agent_with_streaming
from m11_mcp_advanced.mcp_bridge import LangChainMCPAdapter


# ===环境配置===
# 复制当前py进程的环境变量,并在复制的环境变量里新增一条，确保安全可控
env_vars = os.environ.copy()
env_vars["AMAP_MAPS_API_KEY"] = AMAP_MAPS_API_KEY

MCP_SERVER_CONFIGS = [
    # 方式1.1: 云端代理 —— stdio模式
    {
        "name":"高德地图", # 打印使用了什么MCP，可移除
        "transport":"stdio", # 指定传输模式
        "command":"npx",
        "args":["-y", "@amap/amap-maps-mcp-server"],
        "env":env_vars
    }

    # 方式1.2: 云端MCP服务 —— Streamable HTTP模式
    # {
    #     "name":"高德地图",
    #     "transport":"http",
    #     "url": f"https://mcp.amap.com/mcp?key={AMAP_MAPS_API_KEY}"
    # }

    # 方式2.1: 本地工具 —— stdio模式
    # {
    #     "name": "本地天气",
    #     "transport": "stdio",
    #     "command": "python",
    #     "args": ["-m", "m10_mcp_basics.stdio_server"],
    #     "env": None
    # }

    # 方式2.2:本地MCP服务 —— Streamable HTTP 模式
    # {
    #     "name":"本地天气",
    #     "transport":"http",
    #     "url": "http://127.0.0.1:8001/mcp"
    # }
    # {...}  之后MCP工具可随需求扩展增加
]

# ===构建图逻辑===
def build_graph(available_tools):
    """
    这个函数只认tools列表，不关心tools的来源
    """
    if not available_tools:
        print('⚠️ 当前没有注入任何工具，Agent将仅靠LLM回答。')
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com",
        streaming=True
    )
    # 如果没工具，bind_tools 会被忽略或处理，LangGraph同样能正常跑纯对话
    llm_with_tools = llm.bind_tools(available_tools) if available_tools else llm


    sys_prompt = """
    你是一个专业的地理位置服务助手。
    1. 当用户查询模糊地点（如"西站"）时，会优先使用相关工具获取具体经纬度或标准名称。
    2. 如果用户查询"附近"的店铺，请先确定中心点的坐标或具体位置，再进行搜索。
    3. 调用工具时，参数要尽可能精确。
    """

    async def agent_node(state:MessagesState):
        messages = [SystemMessage(content=sys_prompt)] + state["messages"]
        # ainvoke:异步调用版的invoke
        return {"messages":[await llm_with_tools.ainvoke(messages)]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent",agent_node)

    # 动态逻辑：如果有工具才加工具节点，否则就是纯对话
    if available_tools:
        tool_node = ToolNode(available_tools)
        workflow.add_node("tools",tool_node)

        def should_continue(state:MessagesState):
            last_msg = state["messages"][-1]
            if hasattr(last_msg,"tool_calls") and last_msg.tool_calls:
                return "tools"
            return END

        workflow.add_edge(START,"agent")
        workflow.add_conditional_edges("agent",should_continue,{"tools":"tools",END:END})
        workflow.add_edge("tools","agent")
    else:
        workflow.add_edge(START,"agent")
        workflow.add_edge("agent",END)

    return workflow.compile()



# ===主程序===
async def main():
    # 使用ExitStack统一管理所有资源的关闭
    async with AsyncExitStack() as stack:
        # A.插件(MCP)注入阶段 -- 允许为空
        dynamic_tools = await LangChainMCPAdapter.load_mcp_tools(stack,MCP_SERVER_CONFIGS)

        # B.图构建阶段
        app = build_graph(available_tools=dynamic_tools)

        # C.运行阶段(流式)
        query = "帮我查一下杭州西湖附近的酒店"
        await run_agent_with_streaming(app,query)


if __name__ == '__main__':
    asyncio.run(main())