from config import OPENAI_API_KEY,LANGCHAIN_API_KEY
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END,START
from langgraph.prebuilt import ToolNode
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true" # 总开关，决定启用追踪功能
os.environ["LANGCHAIN_PROJECT"] = "demo01" # 自定义项目名
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# LLM配置
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 工具定义
@tool
def get_weather(loaction):
    """模拟获取天气"""
    return f'{loaction}当前天气：23℃，晴，风力2级'


tools = [get_weather]
llm_with_tools = llm.bind_tools(tools) # 让llm学会调用工具节点


# --- 核心组件:拆解AgentExecutor ---
# ReAct Step1:Thought(LLM决策)
def call_model(state:MessagesState):
    response = llm_with_tools.invoke(state['messages'])
    return {"messages":[response]} # 新消息追加到状态


# ReAct Step2-3:Action + Observation
tool_node = ToolNode(tools) # 工具节点函数，langgraph已封装

# ReAct Step4:Loop Controller(是否循环)
def should_continue(state:MessagesState):
    last_msg = state["messages"][-1]
    if hasattr(last_msg,"tool_calls") and len(last_msg.tool_calls) > 0:
        return "tools" # 有工具调用 -> 执行工具
    return END         # 无工具调用 -> 返回答案


# --- 构建 ReAct 循环图---
workflow = StateGraph(MessagesState)

workflow.add_node("agent",call_model) # Thought
workflow.add_node("tools",tool_node) # Action + Observation

workflow.add_edge(START,"agent")

# 条件边:Thought -> 决定下一步
workflow.add_conditional_edges(
    "agent", # 从哪个节点出发
    should_continue, # 决定下一步去哪
    {
        "tools":"tools", # 如果返回tools，去tools节点
        END:END          # 如果返回END，直接结束工作流
    }
)

workflow.add_edge("tools","agent") # 工具调用的结果再返回给agent节点

app = workflow.compile()

if __name__ == '__main__':
    # 触发工具
    result = app.invoke(
        {"messages":[
            HumanMessage(content="北京天气如何?")
        ]}
    )
    print('工具调用结果:',result['messages'][-1].content)
    # 不触发工具
    result = app.invoke({"messages":HumanMessage(content="你好")})
    print('直接回答:',result['messages'][-1].content)