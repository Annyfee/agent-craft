import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()


def create_client():
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def get_weather(location):
    # 模拟获得天气信息
    return f"{location}当前天气：23℃，晴，风力2级"


# 以下格式为固定写法，一般仅需改description与name
get_weather_func = {
    "name": "get_weather",  # 函数名称
    "description": "获取指定城市的天气情况",  # 对该函数的描述
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",  # 该参数类型
                "description": "城市名称，如北京、上海等"  # 对该参数的描述
            }
        },
        "required": ["location"]  # 声明必填
    }
}

# 固定写法，有多少个tool就往里追加多少个
tools = [
    {
        "type": "function",
        "function": get_weather_func
    }
]

def chat_loop(agent_client, tools):
    messages = [
        {"role": "system",
         "content": "你是一个善解人意会热心回答人问题的助手。如果你感觉你回答不了当前问题，就会调用函数来回答。"},
        {"role": "user", "content": "北京今天的天气怎么样?"}
    ]
    response = agent_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,  # 调用工具
        tool_choice="auto"  # 模型自主选择是否调用工具
    )
    message = response.choices[0].message
    # 如果有该参数，证明ai调用了工具
    if message.tool_calls:
        # 对每个可能要调用的工具进行循环
        for tool_call in message.tool_calls:
            if tool_call.function.name == "get_weather":
                # 解析参数
                args = json.loads(tool_call.function.arguments)  # 获取用户关键词的参数
                location = args.get("location", "未知地点")

                # 调用真实参数
                weather_info = get_weather(location)

                # 将函数执行结果以"tool"角色传给模型，等待后面二次调用
                messages.append(message)  # 先添加模型的原始响应
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": weather_info
                })
        # 第二次调用，让模型基于工具返回的结果再生成最终答案
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
