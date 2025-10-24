import os  # 导入环境变量
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# 让ai说一句话
from langchain_openai import ChatOpenAI

# 配置deepseek
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    # 注：在.env里把OPENAI_API_KEY改成你自己的api-key即可
    base_url="https://api.deepseek.com"
)

# 调用模型
response = llm.invoke("你好呀")
print(response.content)