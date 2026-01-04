import streamlit as st

st.set_page_config(page_title="智能客服驾驶舱",layout="wide") # 标签页的命名
st.title("✈️ 智能航天客服 Swarm") # 标题

# 侧边栏
with st.sidebar:
    st.header("📦 驾驶舱监控") # 侧边栏标题
    st.info("当前坐席:前台 TriageAgent") # 侧边栏高亮信息
    st.subheader("用户画像") # 侧边栏副标题
    st.json({"name":"张三","vip":True})

# 画聊天历史(模拟)
with st.chat_message("user",avatar="👤"): # 用一个小表情代表发言人头像
    st.write("我要退票")

with st.chat_message("assistant",avatar="🤖"):
    st.write("好的，为您转接退票专员...")

# 画输入框
prompt = st.chat_input("请输入您的问题")
if prompt:
    # 当用户输入后，页面会刷新，显示下面的内容
    with st.chat_message("user",avatar="👤"):
        st.write(prompt)