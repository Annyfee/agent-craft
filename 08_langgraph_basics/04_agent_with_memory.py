import os
from config import OPENAI_API_KEY,LANGCHAIN_API_KEY
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END,START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver

os.environ["LANGCHAIN_TRACING_V2"] = "true" # 总开关，决定启用追踪功能
os.environ["LANGCHAIN_PROJECT"] = "demo02" # 自定义项目名
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# LLM配置
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# Prompt配置
sys_prompt = "你是一个强大的助手，能查天气，也能回答一般问题。请使用中文回答。"

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
    # 构造带system prompt 的完整消息列表(仅用于本次LLM调用)
    message_for_llm = [SystemMessage(content=sys_prompt)]+state["messages"]
    response = llm_with_tools.invoke(message_for_llm)
    # 此处只会返回新生成的消息，不包含prompt，防止污染历史
    return {"messages":[response]} # 新消息追加到状态


# ReAct Step2-3:Action + Observation
tool_node = ToolNode(tools)

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

workflow.add_edge("tools","agent")





# 编译时启用记忆
app = workflow.compile(checkpointer=MemorySaver())



if __name__ == '__main__':
    session_id = "user123"
    config = {
        "configurable":{"thread_id":session_id}
    }
    while 1:
        user_input = input('\n你：')
        if user_input.strip().lower() == 'quit':
            break

        result = app.invoke(
            {'messages':[HumanMessage(content=user_input)]},
            config=config
        )

        ai_msg = result["messages"][-1]
        print(f'AI：{ai_msg.content}')






