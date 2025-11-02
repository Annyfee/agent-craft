from langchain_huggingface import HuggingFaceEmbeddings

# 第一次运行可能时间较久
print('---正在首次加载本地嵌入模型(bge-small-zh-v1.5)...---')

# 理论：有embedding的向量模型
embeddings_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5" # 一个中英双语开源模型
)
print('嵌入模型载入完毕')

# 演示：将文本转换为向量
text = "模块05的目标是什么"
query_embedding = embeddings_model.embed_query(text)

# 验证：向量存在，而且有具体数值
print(f'文本:{text}')
print(f'向量(前五维):{query_embedding[:5]}')
print(f'向量维度:{len(query_embedding)}')