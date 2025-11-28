from embeddings import get_embeddings
from config import OPENAI_API_KEY
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- 模块A (离线操作) ---
# 1. 加载&分割 2. 向量化 3. 存储
KNOWLEDGE_BASE_CONTENT = """
### 模块 01 - Agent 入门 & 环境搭建
- **目标**: 理解 Agent 概念, 完成环境配置与首次调用。
- **内容**: 环境依赖 | API Key 配置 | 最小可运行 Agent

### 模块 02 - LLM 基础调用
- **目标**: 掌握模型调用逻辑, 初步构建智能体能力。
- **内容**: LLM 了解与调用 | Prompt 编写与逻辑构思 | 多轮对话记忆 | 独立构建一个智能体

### 模块 03 - Function Calling 与工具调用
- **目标**: 实现 LLM 调用外部函数, 赋予模型“执行力”。
- **内容**: Function calling 原理 | 工具函数封装 | API 接入实践 | 多轮调用流程 | Agent 能力扩展

### 模块 04 - LangChain 基础篇
- **目标**: 认识 LangChain 六大模块, 学会用 LangChain 构建智能体。
- **内容**: LLM 调用 | Prompt 设计 | Chain 构建 | Memory 记忆 | 实战练习

### 模块 05 - LangChain 进阶篇
- **目标**: 掌握 LangChain Agents 的核心机制, 构建能调用工具、持续思考、具备记忆的智能体。
- **内容**: Function Calling | @tool 工具封装 | ReAct 循环 | Agent 构建 | SQL Agent | 记忆+流式 | 开发优化
"""
with open("knowledge_base.txt", "w", encoding="utf-8") as f:
    f.write(KNOWLEDGE_BASE_CONTENT)

loader = TextLoader('knowledge_base.txt',encoding='utf8')
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250,chunk_overlap=40)
splits = text_splitter.split_documents(docs)
embedding_model = get_embeddings("bge-small-zh-v1.5")
db = FAISS.from_documents(splits,embedding_model) # 在内存中构建向量索引，但不持久化到本地文件
print('---模块A(Indexing)完成---\n')



# --- 模块B (在线运行:Online R-A-G Flow) ---
print('--- 模块B R-A-G正在构建---\n')

# 1. R (Retrieval - 检索)
retrieve = db.as_retriever(search_kwarg={"k":1}) # 只返回最相关的1个

# 2. A (Augmented - 增强)
system = """
请你扮演一个 Ai Agent 教学助手。
请你只根据下面提供的“上下文”来回答问题。
如果上下文中没有提到，请回答“对不起，我不知道”。

[上下文]:
{context}

[问题]:
{question}
"""
prompt = ChatPromptTemplate.from_messages([
    ('system',system),
    ('human','{question}')
])

# 3. G (Generation - 生成)
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 4. 辅助函数：将检索到的Doc原始文档对象格式化为字符串，让llm能读懂
def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)


# 5. 组装 RAG 链条(LCEL)
rag_chain = (
    {"context":retrieve | format_docs,"question":RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 运行 RAG 链 ---

question = '模块05的目标是什么？'
response = rag_chain.invoke(question)
print(f'提问:{question}')
print(f'回答:{response}\n')

question = 'Langchain进阶篇讲了什么？'
response = rag_chain.invoke(question)
print(f'提问:{question}')
print(f'回答:{response}\n')

question = '今天天气怎么样？'  # 知识库中没有
response = rag_chain.invoke(question)
print(f'提问:{question}')
print(f'回答:{response}\n')

# 清理临时文件
os.remove("knowledge_base.txt")
