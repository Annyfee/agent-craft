from config import OPENAI_API_KEY
import time
from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

# 配置llm
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
# 设置全局缓存
set_llm_cache(InMemoryCache())

# 第一次调用llm(会远程请求)
query = "用中文写一句关于猫的五言诗。"
start_time = time.time()
response1 = llm.invoke(query).content
print(f"第一次调用结果: {response1}")
print(f"第一次运行时间: {time.time() - start_time:.4f} 秒")
print('')

# 第二次调用llm(会命中缓存)
start_time = time.time()
response2 = llm.invoke(query).content
print(f"第二次调用结果: {response2}")
print(f"第二次运行时间 (已缓存): {time.time() - start_time:.4f} 秒")

# 清理
set_llm_cache(None) # 关闭缓存，以免影响后续实例
print('缓存清理完成')














