from config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
# 在LangChain 1.0+版本中，以下俩组件移到了langchain-classic包中
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool # 导入 @tool

# 配置LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 配置prompt
prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个聪明的智能助手。当你遇到解决不了的问题时，会调用工具来解决问题。"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad") # 必加，Agent的思考过程
])

# 配置tool
@tool
def get_weather(location):
    """模拟获得天气信息"""
    return f"{location}当前天气：23℃，晴，风力2级"

@tool
def get_user_name(user):
    """模拟获得用户名字"""
    return f'用户名字是:{user}'


tools = [get_weather,get_user_name]

# 创建Agent(大脑)
agent = create_tool_calling_agent(llm=llm,prompt=prompt,tools=tools)
# 创建AgentExecutor(执行器)--负责运行ReAct循环
agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True) # 开启verbose以看到ai思考链
# 运行
response = agent_executor.invoke({
    'input':"今天北京的天气怎么样？"
})

print(response)
print()
print(response['output'])

