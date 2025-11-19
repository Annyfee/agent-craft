from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from embeddings import get_embeddings
from config import OPENAI_API_KEY
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


Persist_directory = './chroma_db_war_and_peace_bge_small_en_v1.5'
model_name_str = 'BAAI/bge-small-en-v1.5'

if not os.path.exists(Persist_directory):
    print(f"错误: 知识库文件 {Persist_directory} 未找到。")
    print("请先运行'00_build_index.py'生成向量数据库，再运行该文件")
    exit()

print('---加载本地向量数据库---')

# 模块A:链接本地Chroma向量数据库
# 1. 加载 Embedding 模型
print(f'正在加载/下载模型{model_name_str}...')
embeddings_model = get_embeddings(
    model_name=model_name_str,
    device='cpu'
)

# 2. 从本地目录加载Chroma DB
db = Chroma(
    persist_directory=Persist_directory,
    embedding_function=embeddings_model
)
print(f'Chroma数据库已从本地加载(共{db._collection.count()}条)\n')

# 模块B:R-A-G Flow
# 1. R-检索
retriever = db.as_retriever(search_kwargs={"k": 5})  # 召回5条相关数据

# 2. A-增强
sys_prompt = """
你是一个博学的历史学家和文学评论家。
请根据以下上下文回答问题。如果上下文**强烈暗示**了答案，即使未明说，也可推理回答。
如果完全无关，请回答“对不起，根据所提供的上下文我不知道”。

[上下文]: {context}
[问题]: {question}
"""
prompt = ChatPromptTemplate.from_messages([
    ('system', sys_prompt),
    ('human', '{question}')
])

# 3. G-生成
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 4. 辅助函数
def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)


# 5. 组装RAG链条(LCEL)
rag_chain = (
    {"context":retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
# 运行RAG链
print('---正在运行RAG链条---')
question = '莫斯科大火发生在小说的哪一部分？有哪些角色亲历了这场灾难？'
response = rag_chain.invoke(question)
print(f'提问:{question}')
print(f'回答:{response}')