from langchain_core.tools import tool

@tool
def get_weather(location):
    """模拟获得天气信息"""
    return f"{location}当前天气：23℃，晴，风力2级"

@tool
def get_user_name(user):
    """模拟获得用户名字"""
    return f'用户名字是:{user}'


# 封装好要用的工具
tools = [get_weather,get_user_name]
print('工具箱已封装完毕!')