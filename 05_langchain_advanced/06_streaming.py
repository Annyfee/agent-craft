from config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool # 导入 @tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# 配置llm
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)
# 配置prompt(新增俩占位符 一个为对话历史记录，一个为agent的思考过程)
prompt = ChatPromptTemplate.from_messages([
    ('system','你是小智，一个帮助他人的智能助手。当你无法解答当前问题时，会调用工具来解决问题。'),
    MessagesPlaceholder(variable_name="history"),
    ('human','{input}'),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# 配置tool
@tool
def get_weather(location):
    """模拟获得天气信息"""
    return f"{location}当前天气：23℃，晴，风力2级"


tools = [get_weather]
# 配置agent
agent = create_tool_calling_agent(llm=llm,prompt=prompt,tools=tools)
# 配置AgentExecutor
agent_executor = AgentExecutor(agent=agent,tools=tools) # 这里没加verbose=True，想打印日志看思考链的可以自行打印


# 记忆存储--包装agent_executor
store = {}
def get_session_history(session_id:str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


agent_with_memory = RunnableWithMessageHistory(
    runnable=agent_executor,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)
# 打印测试
session_id = 'user123'

if __name__ == '__main__':
    while 1:
        user_input = input('\n你:')
        if user_input == 'quit':
            print('拜拜~')
            break
        # 用于标记"AI:"这个内容
        # flush=True保证"AI:"立即输出，而不是等缓存区存满再输出
        print("AI: ", end="", flush=True)
        response = agent_with_memory.invoke(
            {'input': user_input},
            config={'configurable': {'session_id': session_id}}
        )
        print()

