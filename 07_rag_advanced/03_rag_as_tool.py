import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_core.tools import tool


# 全局 LLM (供Agent和Rag共用)
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# (1) 构建一个可复用的 RAG链条 (P1+P2)
def build_rag_chain(llm_instance):
    print('---正在构建RAG链条...---\n')

    Persist_directory = './chroma_db_war_and_peace_bge_small_en_v1.5'
    Embedding_model = 'BAAI/bge-small-en-v1.5'
    Encoder_model = "BAAI/bge-reranker-base"

    if not os.path.exists(Persist_directory):
        raise FileNotFoundError(f'索引目录{Persist_directory}未找到，请先运行 build_index.py')

    embeddings_model = HuggingFaceEmbeddings(model_name=Embedding_model)
    db = Chroma(
        persist_directory=Persist_directory,
        embedding_function=embeddings_model
    )

    # 1. R-检索--强化版
    base_retriever = db.as_retriever(search_kwargs={"k":5})
    encoder = HuggingFaceCrossEncoder(model_name=Encoder_model)
    reranker = CrossEncoderReranker(model=encoder,top_n=2)
    compression_retriever=ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=reranker
    )
    retriever = compression_retriever

    # 2. A-增强
    sys_prompt = """
    你是一个博学的历史学家和文学评论家。
    请根据以下上下文回答问题。如果上下文**强烈暗示**了答案，即使未明说，也可推理回答。
    如果完全无关，请回答“对不起，根据所提供的上下文我不知道”。
    
    [上下文]: {context}
    [问题]: {question}
    """
    prompt = ChatPromptTemplate.from_messages([
        ('system',sys_prompt),
        ('human','{question}')
    ])
    # 3.G-生成(llm已在全局生成)

    # 4. 辅助函数
    def format_docs(docs):
        return '\n'.join(doc.page_content for doc in docs)

    # 5.组装RAG链条
    rag_chain = (
        {'context':retriever | format_docs, 'question': RunnablePassthrough()}
        | prompt
        | llm_instance
        | StrOutputParser()
    )
    print('---RAG链条构建完毕!---\n')
    return rag_chain


#    初始化RAG链
rag_chain_instance = build_rag_chain(llm)

# (2) 封装为标准 Langchain Tool
@tool
def search_war_and_peace(query):
    """查询《战争与和平》小说中的内容，包括人物、情节、历史事件等"""
    print(f'\n正在检索《战争与和平》:{query}')
    return rag_chain_instance.invoke(query)

# 也可以与其他工具并列使用
@tool
def get_weather(location):
    """模拟获得天气信息"""
    return f"{location}当前天气：23℃，晴，风力2级"


tools = [search_war_and_peace,get_weather]


# 运行
if __name__ == '__main__':
    question = "皮埃尔是共济会成员吗？他在其中扮演什么角色？"
    res = search_war_and_peace.invoke(question)
    print(f'问题:{question}')
    print(f'回答:{res}')




























