import os
import time
from config import OPENAI_API_KEY,LANGCHAIN_API_KEY
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages

# LangSmith调试
os.environ["LANGCHAIN_TRACING_V2"] = "true" # 总开关，决定启用追踪功能
os.environ["LANGCHAIN_PROJECT"] = "supervisor_agent_ops_system" # 自定义项目名
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# === 一、Graph-as-a-Tool ===
# === 模拟一个不稳定的SSH日志查询过程 ===

class SSHState(TypedDict):
    target_ip: str
    attempt: int
    logs: str

def connect_ssh(state:SSHState):
    """模拟SSH连接，第一次连接必定超时"""
    print(f'    [子图]正在尝试连接服务器{state["target_ip"]}(第{state["attempt"]}次)')
    if state['attempt'] == 1:
        return {'logs':'ERROR:Connection Timed Out','attempt':state['attempt']+1}
    return {'logs':'CONNECTED','attempt':state['attempt']+1}

def grep_system_logs(state:SSHState):
    """连接成功后读取日志"""
    if state["logs"] == "CONNECTED":
        # 打印查到的结果
        return {'logs':f'SUCCESS: Retrieved logs from {state["target_ip"]}:[ERROR: OutOfMemory at line 4032]'}
    return {'logs':state['logs']} # 保持错误状态

def ssh_routing(state:SSHState):
    """路由逻辑：如果连接失败且尝试次数少于3，重试"""
    if "ERROR" in state['logs'] and state["attempt"] <= 2:
        return "connect"
    return "grep"

# 构建子图
ssh_workflow = StateGraph(SSHState)
ssh_workflow.add_node("connect",connect_ssh)
ssh_workflow.add_node("grep",grep_system_logs)

ssh_workflow.add_edge(START,"connect")
ssh_workflow.add_conditional_edges("connect",ssh_routing,{"connect":"connect","grep":"grep"})
ssh_workflow.add_edge("grep",END)

ssh_app = ssh_workflow.compile()

# 将子图封装为工具
@tool
def analyze_server_logs(ip_address:str):
    """使用SSH连接服务器并分析最近的错误日志（内含自动重连机制）"""
    result = ssh_app.invoke({"target_ip":ip_address,"attempt":1,"log":""})
    return result['logs']



# === 二、Human-in-the-Loop ===
# === 重启服务，高危操作，需要审批 ===

@tool
def restart_service(service_name:str):
    """重启指定的服务器服务"""
    return f"服务[{service_name}]已成功重启，系统负载已恢复正常"



# === 三、Multi-Agent 编排 ===
# === 总控调度 + 专家分工 ===

# 1. 共享状态
class AgentState(TypedDict):
    messages:Annotated[list,add_messages]
    next_speaker:str

# 2. 专家节点
def log_expert(state:AgentState):
    prompt = "你是日志分析专家，使用工具分析服务器日志，找出报错原因。回答需简洁。"
    messages = [SystemMessage(content=prompt)] + state['messages']
    # 绑定子图工具
    tools = [analyze_server_logs]
    response = llm.bind_tools(tools).invoke(messages)
    return {"messages":[response]}

def ops_expert(state:AgentState):
    prompt = "你是运维专家。当收到修复指令时，请立即调用 'restart_service' 工具进行修复，不要输出任何额外的解释文本。"
    messages = [SystemMessage(content=prompt)] + state['messages']
    tools = [restart_service]
    # 绑定敏感工具
    response = llm.bind_tools(tools).invoke(messages)
    return {"messages":[response]}

# 3. 总控节点（supervisor）
def supervisor(state:AgentState):
    prompt = """
    你是 IT 运维总指挥。
    专家列表：
    - log_expert
    - ops_expert

    决策逻辑：
    1. 未知原因 -> log_expert
    2. 已知原因（如OOM、报错） -> ops_expert
    3. 修复完成 -> FINISH

    【输出约束】
    仅输出下一个专家的名字（如 log_expert），不要包含任何其他字符或标点。
    """
    messages = [SystemMessage(content=prompt)] + state['messages']
    response = llm.invoke(messages)
    return {"next_speaker":response.content.strip()}

# 4. 路由逻辑
def route_supervisor(state:AgentState):
    if state['next_speaker'] == "FINISH":
        return END
    return state['next_speaker']

def should_continue(state:AgentState):
    last_msg = state['messages'][-1]
    if hasattr(last_msg,"tool_calls") and last_msg.tool_calls:
        return "tools"
    return "supervisor"

def route_after_tool(state:AgentState):
    return state["next_speaker"]


# === 四、构建主图与集成 ===

# 工具集合
all_tools = [analyze_server_logs,restart_service]
tool_node = ToolNode(all_tools)

# 构建主图
workflow = StateGraph(AgentState)

workflow.add_node("supervisor",supervisor)
workflow.add_node("log_expert",log_expert)
workflow.add_node("ops_expert",ops_expert)
workflow.add_node("tools",tool_node)

workflow.add_edge(START,"supervisor")
workflow.add_conditional_edges("supervisor",route_supervisor)
for member in ["log_expert","ops_expert"]:
    workflow.add_conditional_edges(
        member,
        should_continue,
        {"tools":"tools","supervisor":"supervisor"}
    )
workflow.add_conditional_edges("tools",route_after_tool)

# 编译图:加入记忆与中断机制(Human-in-the-Loop)
# 注: 我们在所有工具执行前都暂停，但在运行时进行逻辑判断
app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"]
)

# === 五、运行时逻辑(模拟生产环境的交互) ===

if __name__ == '__main__':
    # 模拟一次完整的故障处理流程
    user_input = "服务器 192.168.1.100 报警，响应极慢，请处理。"
    config = {
        "configurable": {"thread_id": "incident_001"}
    }

    print(f'收到报警 : {user_input}')
    inputs = {"messages":[HumanMessage(content=user_input)]}

    # 循环执行，直到任务结束
    while 1:
        # 1. 执行图直到中断或结束
        for _ in app.stream(inputs,config,stream_mode="values"):
            pass

        # 2. 检查当前状态
        snapshot = app.get_state(config)
        next_tasks = snapshot.next

        # 没有下一步，任务结束
        if not next_tasks:
            print(f"    最终报告:{snapshot.values['messages'][-1].content}")
            break

        # 3. 处理中断:判断是哪个工具被调用
        if "tools" in next_tasks:
            last_msg = snapshot.values['messages'][-1]
            tool_call = last_msg.tool_calls[0]
            tool_name = tool_call["name"]

            print(f'\n[系统暂停] 请求调用工具:{tool_name}')

            # 策略A: 自动放行安全工具(Graph-as-a-Tool)
            if tool_name == "analyze_server_logs":
                print('     -> 这是一个查询类工具，系统自行批准。')
                inputs = None # 继续执行
                continue

            # 策略B: 拦截高危工具(Human-in-the-Loop)
            elif tool_name == "restart_service":
                print("     -> ⚠️ 警告: 这是一个高危操作!")
                user_approval = input("     -> 请人工审批 (输入 'yes' 允许重启):")

                if user_approval == "yes":
                    print('    -> ✅ 审批通过，正在执行...')
                    inputs = None # 继续执行
                else:
                    print('    -> ❌️ 审批拒绝，任务终止!')
                    # 实际系统中，应通过 ToolMessage 反馈人工拒绝，使 LLM 能继续响应；
                    # 当前demo为简化，直接退出
                    break