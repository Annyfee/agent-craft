import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents import Runner, set_tracing_disabled
from agents.agent import Agent
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

set_tracing_disabled(True)

# 初始化模型
client = AsyncOpenAI(api_key=OPENAI_API_KEY,base_url="https://api.deepseek.com")
model = OpenAIChatCompletionsModel(model="deepseek-chat",openai_client=client)

# 定义一个通用Agent
smart_agent = Agent(
    name="SmartAssistant",
    instructions="""
        你是航空公司智能客服助手，客户姓名：张三（白金会员），航班号：CA1234。

        你具备以下能力：
        - 用户说“退票”“退款”“取消” → 回复：✅ 退款申请已提交，预计3个工作日内原路返回。
        - 用户说“改签”“换航班” → 回复：✅ 明日同航线航班尚有余座，已为您预留，可随时确认改签。
        - 其他任何问题 → 礼貌、专业地直接回答

        回复要简洁、自然、带表情符号，让用户感到温暖。
        """,
    model=model
)

# Streamlit UI组件
st.set_page_config(page_title="智能客服驾驶舱",layout="wide") # 标签页命名
st.title("✈️ 智能航天客服 Swarm") # 页面标题

# 侧边栏:驾驶舱监控(先固定不变动)
with st.sidebar:
    st.header("🖥️ 驾驶舱监控")
    st.success("当前坐席: 智能助理 SmartAssistant 🤖") # success用作高亮块显示
    st.subheader("用户画像")
    st.json({"user_name": "张三(白金会员)", "flight_no": "CA1234"})

# 会话状态与历史消息
if "messages" not in st.session_state: # 首次运行时，初始化空列表，用于存储聊天消息。
    st.session_state["messages"] = []

for msg in st.session_state["messages"]: # 重新渲染历史消息，确保聊天上下文在页面刷新后依然可见
    avatar = "👤" if msg['role'] == 'user' else "🤖"
    with st.chat_message(msg['role'],avatar=avatar):
        st.write(msg["content"])

# 用户输入与核心交互
prompt = st.chat_input("请输入您的问题（试试：我要退票 / 想改签 / 你好）")
if prompt:
    # 显示用户信息
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user",avatar="👤"):
        st.write(prompt)

    # 调用Agents SDK
    with st.spinner("思考中..."): # 执行耗时操作时，显示旋转的加载动画
        result = Runner.run_sync( # 同步运行智能体
            smart_agent, # 参数:agent
            st.session_state.messages # 参数:对话历史
        )

    # 显示AI回复
    reply = result.final_output # 最终AI回复内容
    st.session_state.messages.append({"role":"assistant","content":reply})
    with st.chat_message("assistant",avatar="🤖"):
        st.write(reply)