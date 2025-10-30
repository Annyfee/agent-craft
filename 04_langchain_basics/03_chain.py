import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 定义提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你非常可爱，说话末尾会带个喵"),
    ("human", "{input}")  # {input}:占位符
])

# 初始化模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 定义解析器，把LLM返回的AIMessage转成字符串
parser = StrOutputParser()

# 组成Chain
chain = prompt | llm | parser

# 最终调用
result = chain.invoke({"input": "你好喵"})
print(result)
