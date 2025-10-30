import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory


prompt = ChatPromptTemplate.from_messages([
    ("system", "你非常可爱，说话末尾会带个喵"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")  # {input}:占位符
])
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com"
)
parser = StrOutputParser()

chain = prompt | llm | parser

# 存储所有会话历史(可用数据库替换)
# 此处用字典模拟，也可替换成Redis、SQL等
store = {}

def get_session_history(session_id:str):
    """根据session_id获取该用户的聊天历史"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory() # 创建新的历史记录
    return store[session_id]


# 包装成带记忆的Runnable
runnable_with_memory = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

session_id = 'user_123'
while 1:
    user_input = input("\n你:")
    if user_input=="quit":
        print('拜拜喵!')
        break
    response = runnable_with_memory.invoke(
        {"input":user_input},
        config={"configurable":{"session_id":session_id}}
    )
    print(f'AI:{response}')





























