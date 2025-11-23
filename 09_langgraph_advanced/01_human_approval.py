import os
from config import OPENAI_API_KEY,LANGCHAIN_API_KEY
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# LangSmith调试
os.environ["LANGCHAIN_TRACING_V2"] = "true" # 总开关，决定启用追踪功能
os.environ["LANGCHAIN_PROJECT"] = "human_approval" # 自定义项目名
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# llm配置
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)


# 定义一个敏感工具：发送邮件(模拟)
@tool
def send_email(to, content):
    """模拟发送邮件"""
    return f'邮件已发送至{to},内容为：{content}'


# 工具绑定到llm
tools = [send_email]
llm_with_tools = llm.bind_tools(tools)

# Node函数与Edge节点
tool_node = ToolNode(tools)


def call_model(state: MessagesState):
    response = llm_with_tools.invoke(state['messages'])
    return {"messages":[response]}


def should_continue(state: MessagesState):
    last_msg = state['messages'][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return END



# 构建基础ReAct图
workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge("tools", "agent")

app = workflow.compile(
    # 在内存里做状态持久化
    checkpointer=MemorySaver(),
    interrupt_before=["tools"] # 选择要人工审批的节点 -- 负责在哪里停，之后的代码负责停了之后怎么办
)


if __name__ == '__main__':
    config = {
        "configurable":{"thread_id":"user123"}
    }
    user_input = "请帮我给 boss@example.com 发一封邮件，内容是：会议推迟到明天下午3点。"

    print("用户输入:",user_input)
    print("\nAgent正在思考...\n")

    # 初识输入
    inputs = {"messages":[HumanMessage(content=user_input)]}

    while 1:
        # 触发工作流执行，推进到下一个中断点或自然结束
        # inputs注入事件;config确定回话id;"values":完整记录每步结果
        for _ in app.stream(inputs,config,stream_mode="values"): # 流式执行
            pass   # 必须迭代生成器，才能实际执行工作流

        # 获取当前状态
        snapshot = app.get_state(config)
        next_tasks = snapshot.next # 返回下一步要执行的节点名列表

        # 如果没有下一步，说明工作流已结束
        if not next_tasks:
            final_msg = snapshot.values['messages'][-1]
            print(f'\n最终回复:{final_msg.content}')
            break

        # 如果下一步是需要审批的节点
        if "tools" in next_tasks:
            last_msg = snapshot.values['messages'][-1]
            tool_call = last_msg.tool_calls[0]
            print(f'\n⚠️ Agent准备执行操作：')
            print(f'    工具名称：{tool_call["name"]}')
            print(f'    参数：{tool_call["args"]}')

            approval = input("\n✅ 是否批准执行？(输入 'yes' 继续，其他取消): ").strip().lower()
            if approval == "yes":
                print('\n 继续执行...')
                inputs = None # 表示从断点继续，无新输入
            else:
                print("\n❌ 操作已取消，流程终止")
                break