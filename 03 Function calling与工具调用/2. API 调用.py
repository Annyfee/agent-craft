from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests

load_dotenv()

def create_client():
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 通过api调用获得当前ip与位置
def get_addr():
    res_ip = requests.get('https://ipapi.co/ip/').text
    res_city = requests.get('https://ipapi.co/city/').text
    return f'ip地址:{res_ip},所在城市:{res_city}'


get_addr_func = {
    "name": "get_addr",  # 函数名称
    "description": "获取用户的ip地址与城市",  # 对该函数的描述
    "parameters": {
        "type": "object",
        "properties": {}, # 参数为空，那么这两个地方也是空的
        "required": []
    }
}

tools = [
    {
        "type":"function",
        "function":get_addr_func
    }
]

def chat_loop(agent_client,tools):
    messages = [
        {"role": "system","content": "你是一个善解人意会热心回答人问题的助手。如果你感觉你回答不了当前问题，就会调用函数来回答。"},
        {"role": "user", "content": "我现在在哪个城市，ip地址是多少?"}
    ]
    response = agent_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.function.name == "get_addr":
                # 解析参数
                # args = json.loads(tool_call.function.arguments)  # 获取用户关键词的参数
                # location = args.get("location")
                # 调用真实参数
                # your_info = get_weather(location)

                # 这里无参数，直接调用函数就行
                your_info = get_addr()
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": your_info
                })
                final_res = agent_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages
                )
                print('已调用工具...')
                print(f'回答:{final_res.choices[0].message.content}')
    else:
        # 模型没有要调用工具，直接返回
        print('未调用工具...')
        print(f'回答:{response.choices[0].message.content}')


if __name__ == '__main__':
    client = create_client()
    chat_loop(client, tools)


