import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI

# 初始化模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 调用模型
response = llm.invoke('你好喵')
print(response.content)
