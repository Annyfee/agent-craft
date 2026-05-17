from config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"}, # 提示词角色
        {"role": "user", "content": "Hello"}, # 用户输入的对话
    ],
    stream=False # 非流式输出, 只会等语句全部生成才返回
)

if not response.choices or response.choices[0].message is None:
    raise ValueError("LLM returned empty or filtered response")
print(response.choices[0].message.content)