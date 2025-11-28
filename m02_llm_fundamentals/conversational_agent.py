from config import OPENAI_API_KEY
from openai import OpenAI

def create_client():
    return OpenAI(api_key=OPENAI_API_KEY,base_url="https://api.deepseek.com")

def chat_loop(agent_client):
    messages = [
                {"role":"system","content":"你是一个历史老师，你会耐心的教导我有关的事情。同时你的回答会相对精简，在五十字内。"},
                {"role":"user","content":"汉朝存在了多久，其中哪个皇帝你认为最厉害？"}
            ]
    while 1:
        response = agent_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        answer = response.choices[0].message.content
        print(f'回答:{answer}')

        # 询问是否还有其他问题
        user_input =input('您还有其他想继续问的吗 | (exit退出)\n')
        if user_input == "exit":
            break

        # 继续记录对话(涵盖用户追问 + ai上句回答)
        messages.append({"role":"user","content":user_input})
        messages.append({"role":"assistant","content":answer})


if __name__ == '__main__':
    client = create_client()
    chat_loop(client)
