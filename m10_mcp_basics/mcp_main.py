import os
import sys
from contextlib import AsyncExitStack
import asyncio

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.prebuilt import ToolNode

from config import OPENAI_API_KEY,AMAP_MAPS_API_KEY
from m10_mcp_basics.agent_stream import run_agent_with_streaming
from m10_mcp_basics.mcp_client import MCPClient
from m10_mcp_basics.mcp_bridge import LangChainMCPAdapter



# ===环境配置===
# 环境兼容
COMMAND = "npx.cmd" if sys.platform == "win32" else "npx"
# 复制当前py进程的环境变量,并在复制的环境变量里新增一条，确保安全可控
env_vars = os.environ.copy()
env_vars["AMAP_MAPS_API_KEY"] = AMAP_MAPS_API_KEY

MCP_SERVER_CONFIGS = [
    {
        "name":"高德地图", # 打印使用了什么MCP，可移除
        "command":COMMAND,
        "args":["-y", "@amap/amap-maps-mcp-server"],
        "env":env_vars
    }
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


# ===MCP工具批量初始化===
async def load_mcp_tools(stack:AsyncExitStack,configs:list):
    """
    负责遍历配置，批量建立连接，收集所有工具。
    使用stack将连接生命周期托管给上层
    """
    all_tools = []
    for conf in configs:
        print(f'🔌 正在连接:{conf["name"]}...')
        # 初始化 Client
        client = MCPClient(
            command=conf["command"],
            args=conf["args"],
            env=conf.get("env") # 可选参数
        )
        # 🔥:enter_async_context 替代了async with 缩进
        # 这样无论有多少个MCP，代码层级都不会变深
        adapter = await stack.enter_async_context(LangChainMCPAdapter(client))
        # 批量获取一个MCP下的所有工具
        tools = await adapter.get_tools()
        print(f'    ✅️ 获取工具{[t.name for t in tools]}')
        all_tools.extend(tools)

    return all_tools

# ===主程序===
async def main():
    # 使用ExitStack统一管理所有资源的关闭
    async with AsyncExitStack() as stack:
        # A.插件(MCP)注入阶段 -- 允许为空
        dynamic_tools = await load_mcp_tools(stack,MCP_SERVER_CONFIGS)

        # B.图构建阶段
        app = build_graph(available_tools=dynamic_tools)

        # C.运行阶段(流式)
        query = "帮我查一下杭州西湖附近的酒店"
        await run_agent_with_streaming(app,query)


if __name__ == '__main__':
    asyncio.run(main())