import config
import os
from langchain_community.document_loaders import TextLoader # 加载
from langchain_text_splitters import RecursiveCharacterTextSplitter # 分割


# 创建一个演示txt文件
knowledge_base_content = """
### 模块 01 — Agent 入门 & 环境搭建

- **目标**：理解 Agent 概念，完成环境配置与首次调用。
- **内容**：环境依赖｜API Key 配置｜最小可运行 Agent

### 模块 02 — LLM 基础调用

- **目标**：掌握模型调用逻辑，初步构建智能体能力。
- **内容**：LLM了解与调用｜Prompt编写与逻辑构思｜多轮对话记忆｜独立搭建一个智能体

### 模块 03 — Function Calling 与工具调用

- **目标**：实现 LLM 调用外部函数，赋予模型“执行力”。
- **内容**：Function calling原理｜工具函数封装｜API接入实践｜多轮调用流程｜Agent能力扩展

### 模块 04 — LangChain 基础篇

- **目标**：认识Langchain六大模块，学会用Langchain构建智能体。
- **内容**：LLM 调用｜Prompt 设计｜Chain 构建｜Memory 记忆｜实战练习

### 模块 05 — LangChain 进阶篇

- **目标**：掌握Langchain Agents的核心机制，构建能调用工具、持续思考、具备记忆的智能体。
- **内容**：Function Calling｜@tool 工具封装｜ReAct 循环｜Agent 构建｜SQL Agent｜记忆+流式｜开发优化

"""


with open('knowledge_base.txt','w',encoding='utf8') as f:
    f.write(knowledge_base_content)

# 1.加载
# TextLoader 读取.txt文件，并将其转换为Document对象
loader = TextLoader('knowledge_base.txt',encoding='utf8')
docs = loader.load()
print(f'{docs}已加载完成!')

# 2.分割
text_splitter = RecursiveCharacterTextSplitter(
    # 本节重点
    chunk_size=250, # 设定的chunk块大小(字符数),
    chunk_overlap=40 # 设定的重叠大小(字符数)
) # 创建分割器的配置模板
splits = text_splitter.split_documents(docs) # 实际执行切割

print(f'分块结果:{len(splits)}')

for i,doc in enumerate(splits):
    print(f'片段{i+1}(长度:{len(doc.page_content)})')
    print(doc.page_content)
    print('-'*100+'\n')


# 观察：
# 我们的文本被分割成了四块，没有一块的长度超过250.
# 所以没有用到overlap(重叠)，这是最好的结果

# 删除txt文件
os.remove('knowledge_base.txt')
















