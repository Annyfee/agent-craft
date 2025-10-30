import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

import sqlite3
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase  # 导入 SQLDatabase

# 配置llm
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 创建一个临时的数据库--用于演示
db_file = "test_sql.db"
if os.path.exists(db_file):
    os.remove(db_file)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INT,name TEXT,age INT);")
cursor.execute("INSERT INTO users (id,name,age) VALUES (1,'Alice',30);")
cursor.execute("INSERT INTO users (id,name,age) VALUES (2,'Bob',25);")
conn.commit()
conn.close()

# 连接数据库 -- LangChain 使用 SQLAlchemy URI (连接方式)
db_uri = f'sqlite:///{db_file}'
db = SQLDatabase.from_uri(db_uri)

# 创建sqlAgent -- 一键完成，无需定义tools，仅告诉它使用openai-tools,即Tool Calling(工具调用)模式
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True
)

# 运行
response = agent_executor.invoke({"input":"告诉我Alice多大了？"})
print(response['output'])

# 清理
db._engine.dispose() # 关闭连接池，避免文件被占用
if os.path.exists(db_file):
    os.remove(db_file)
