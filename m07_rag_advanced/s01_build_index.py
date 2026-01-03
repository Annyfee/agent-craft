import config
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from embeddings import get_embeddings


knowledge_base_file = "war_and_peace.txt"
# 持久化目录: Chroma会把所有数据(向量+文本+元数据)都存到这个文件夹
persist_directory = './chroma_db_war_and_peace_bge_small_en_v1.5'
model_name_str = 'BAAI/bge-small-en-v1.5' # 如果愿意等待，可以换成模型"BAAI/bge-m3"，效果更好更适合长文，但下载时间也更久(2.2G)
chunk_size = 500
chunk_overlap = 75


# 检查是否已创建
if os.path.exists(persist_directory):
    print(f"检测到已存在的向量数据库: {persist_directory}")
    print("跳过索引构建。如需重新构建，请手动删除该目录。")
    exit()

if not os.path.exists(knowledge_base_file):
    print(f"错误: 知识库文件 {knowledge_base_file} 未找到。")
    print("请从 https://www.gutenberg.org/ebooks/2600.txt.utf-8 下载")
    print("并重命名为 war_and_peace.txt 放在当前目录。")
    exit()

print('---正在构建索引---')

# 1. 加载
loader = TextLoader(knowledge_base_file,encoding='utf8')
docs = loader.load()
print('加载完成...\n')
# 2. 分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
splits = text_splitter.split_documents(docs)
print('分割完成...\n')
# 3. 向量化 -- 第一次运行会下载模型,预计耗时2分钟
print(f'正在加载/下载模型{model_name_str}...')
embedding_model = get_embeddings(
    model_name=model_name_str,
    device='cpu', # 强制模型在cpu上运行
    encode_kwargs={'batch_size':64} # 每次处理64个文本片段
)
print('Embedding模型加载完成...\n')
# 4. 存储
print('正在构建Chroma索引...(注：此步耗时较久，预计要3min)\n')
db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model
)

#   分批添加切片chunks（每批不超过 5000）
batch_size = 5000  # 必须 < 5461
for i in range(0, len(splits), batch_size):
    batch = splits[i:i + batch_size]
    db.add_documents(batch)
    print(f"已插入 {min(i + batch_size, len(splits))} / {len(splits)} 条")


print(f'✅ 索引构建完毕，共 {len(splits)} 条，已保存到 {persist_directory}')