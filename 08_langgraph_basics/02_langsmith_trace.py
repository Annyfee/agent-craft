from config import OPENAI_API_KEY,LANGCHAIN_API_KEY
from typing import TypedDict
from langgraph.graph import StateGraph,END,START
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true" # 总开关，决定启用追踪功能
os.environ["LANGCHAIN_PROJECT"] = "my_demo" # 自定义项目名
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY


# 1. 定义State(状态) -- 白板上只有一个字段"count"
class State(TypedDict):
    count:int

# 2. 编写Node(节点) -- 两个"工人"
def node_a(state:State):
    # 接收当前State状态，返回要更新的部分
    print(f'[Node A]收到状态：{state}')
    return {"count":state["count"]+1}

def node_b(state:State):
    print(f'[Node B]收到状态：{state}')
    return {"count":state["count"]+1}


# 3. 添加Node到图中
workflow = StateGraph(State) # 创建画布
workflow.add_node("A",node_a) # 添加节点A
workflow.add_node("B",node_b) # 添加节点B

# 4. 用Edge连线
workflow.add_edge(START,"A") # START -> A
workflow.add_edge("A","B") # A -> B
workflow.add_edge("B",END) # B -> END

# 编译成可运行应用
app = workflow.compile()

# 传入初始状态，执行工作流
print("---开始执行---")
result = app.invoke({"count":1})
print("最终状态:",result) # 输出{'count':4}

