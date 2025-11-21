import os
from dotenv import load_dotenv

# 1. 加载.env文件
load_dotenv()

# 2. 解决 UUID v7 警告
try:
    from langsmith import uuid7
    import uuid
    uuid.uuid4 = uuid7 # 全局替换
except ImportError:
    pass # 如果没装 langsmith，省略

# 3. 获取API_KEYS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("× 请在.env中设置OPENAI_API_KEY")
if not LANGCHAIN_API_KEY:
    raise ValueError("× 请在.env中设置LANGCHAIN_API_KEY")












