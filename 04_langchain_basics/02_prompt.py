import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


from langchain_core.prompts import ChatPromptTemplate

# 定义提示词模板(推荐写法)
prompt = ChatPromptTemplate.from_messages([
        ("system","你非常可爱，说话末尾会带个喵"),
        ("human","{input}") # {input}:占位符
])
# 格式化输出
formatted_prompt = prompt.invoke({"input":"你好喵"})
print(formatted_prompt)















