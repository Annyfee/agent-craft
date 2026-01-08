import os
from config import OPENAI_API_KEY,LANGCHAIN_API_KEY
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# LangSmith调试
os.environ["LANGCHAIN_TRACING_V2"] = "true" # 总开关，决定启用追踪功能
os.environ["LANGCHAIN_PROJECT"] = "graph_as_tool" # 自定义项目名
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# llm配置
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 构建子工作流
# 1.子任务状态
class RetryState(MessagesState):
    query: str
    attempt: int
    result: str

# 2.子图逻辑 -- 模拟一个可能失败，需重试的API调用
def call_unstable_api(state:RetryState):
    """模拟偶发性的外部服务，偶发失败"""
    attempt = state["attempt"]
    if attempt == 1:
        # 第一次故意失败
        return {"result":"ERROR：服务暂时不可用","attempt":attempt+1}
    else:
        # 第二次成功
        return {"result":f"SUCCESS：成功处理请求：{state['query']}","attempt":attempt+1}

def should_retry(state:RetryState):
    if "ERROR" in state["result"] and state["attempt"] <= 2: # 出现报错且重试次数小于2，重连
        return "call_api"
    return END

# 3.构建子图工作流
retry_workflow = StateGraph(RetryState)
retry_workflow.add_node("call_api",call_unstable_api)
retry_workflow.add_edge(START,"call_api")
retry_workflow.add_conditional_edges(
    "call_api",
    should_retry,
    {"call_api":"call_api",END:END}
)
retry_app = retry_workflow.compile()

# 4.封装为tool(Graph-as-a-Tool)
@tool
def create_order(query:str) -> str:
    """创建新订单，自动重试保障成功率"""
    result = retry_app.invoke({"query":query,"attempt":1,"result":""})
    return result["result"]


# 5.主graph
tools = [create_order]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

def agent_node(state:MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages":[response]}

def should_continue(state:MessagesState):
    last_msg = state["messages"][-1]
    if hasattr(last_msg,"tool_calls") and last_msg.tool_calls:
        return "tools"
    return END

# 构建主工作流
workflow = StateGraph(MessagesState)
workflow.add_node("agent",agent_node)
workflow.add_node("tools",tool_node)
workflow.add_edge(START,"agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)
workflow.add_edge("tools","agent")

app = workflow.compile()


# 运行
if __name__ == '__main__':
    user_input = "请创建一个新订单：购买三本书"
    print('用户输入:',user_input)

    inputs = {"messages":[
        SystemMessage(content="你是一个任务执行助手。当用户提出任何需要处理、操作或执行的请求时，必须调用 create_order 工具来完成，不要自行回答细节"),
        HumanMessage(content=user_input)
    ]}
    result = app.invoke(inputs)

    tool_result = None
    # 在主工作流的消息历史中，查找最近的工具执行结果
    for msg in reversed(result["messages"]):
        if msg.type == "tool": # 找到ToolMessage类型消息
            tool_result = msg.content
            break
    if tool_result:
        print(f"\n✅ 直接获取子图返回值:\n{tool_result}")
    else:
        print("\n❌ 未执行任何工具")
    final_reply = result["messages"][-1]
    print(f'\n最终回复:\n{final_reply}')