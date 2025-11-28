from embeddings import get_embeddings


# 首次运行可能时间较久 -- 同时运行本文件需要梯子，不然无法加载到本地
print('---正在加载本地嵌入模型(bge-small-zh-v1.5)...---')

# 理论：有embedding的向量模型
embeddings_model = get_embeddings("bge-small-zh-v1.5")
print('嵌入模型载入完毕')

# 演示：将文本转换为向量
text = "模块05的目标是什么"
query_embedding = embeddings_model.embed_query(text)

# 验证：向量存在，而且有具体数值
print(f'文本:{text}')
print(f'向量(前五维):{query_embedding[:5]}')
print(f'向量维度:{len(query_embedding)}')