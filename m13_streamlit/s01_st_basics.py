import streamlit as st

# === 输入框 === st.chat_input
prompt =  st.chat_input("请输入问题")
if prompt:
    # 处理用户输入
    st.write(f"你输入了:{prompt}")


# === 气泡 === st.chat_messages:自动生成对话气泡
# 用户气泡
with st.chat_message("user", avatar="👤"):
    st.write("你是人吗")

# 助手气泡
with st.chat_message("assistant", avatar="🤖"):
    st.write("似乎不太像是人")


# === 折叠状态栏 === st.status:收纳中间步骤
with st.status("Agent 正在思考...",expanded=True): # expanded:默认是否打开折叠栏
    st.write("正在查询数据库...")
    st.write("正在转接专员...")
    # 最终更新状态
    st.success("处理完成")


# === 动态占位符 === st.empty():先占位,后续更新
import time
response = st.empty()
for msg in ["处理中...", "完成！"]:
    response.markdown(msg)
    time.sleep(1)


# === 记忆中枢 === st.session_state:状态持久化
# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 读写
st.session_state.messages.append({"role":"user","content":prompt})


# === 侧边栏 === st.sidebar
with st.sidebar:
    st.write('我是侧边栏')
    st.json({'User':"张三"})

# === 状态同步器 === st.rerun():让UI与最新状态同步
st.session_state.cur_agent = "Refund"
# 注意：在聊天机器人等交互场景中，通常这样写（安全）：
# if some_condition:      # 只有在用户提交新消息后
#     st.session_state.cur_agent = "RefundAgent"
#     st.rerun()          # 手动刷新，显示最新状态

# 如果像上面这样无条件调用 st.rerun()，会造成无限循环刷新，
# 所以这里注释掉，仅用于静态演示。
# st.rerun()