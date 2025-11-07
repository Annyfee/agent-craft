import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_core.tools import tool

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory



# 1. 构建一个可复用的 RAG链条
def build_rag_chain(llm_instance):
    print('---正在构建RAG链条---')

    Persist_directory = './chroma_db_war_and_peace_bge_small_en_v1.5'
    Embedding_model = 'BAAI/bge-small-en-v1.5'
    Encoder_model = "BAAI/bge-reranker-base"

    if not os.path.exists(Persist_directory):
        raise FileNotFoundError(f'索引目录{Persist_directory}未找到，请先运行 build_index.py')

    embedding_model = HuggingFaceEmbeddings(model_name=Embedding_model)
    db = Chroma(
        persist_directory=Persist_directory,
        embedding_function=embedding_model
    )
    # R
    base_retriever = db.as_retriever(search_kwargs={'k':5})
    encoder = HuggingFaceCrossEncoder(model_name=Encoder_model)
    reranker = CrossEncoderReranker(model=encoder,top_n=2)
    compression_retriever = ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=reranker
    )
    retriever = compression_retriever
    # A
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

    def format_docs(docs):
        return '\n'.join(doc.page_content for doc in docs)

    # R-A-G
    rag_chain = (
        {'context':retriever | format_docs,'question':RunnablePassthrough()}
        | prompt
        | llm_instance
        | StrOutputParser()
    )
    print('---RAG链条构建完毕!---\n')
    return rag_chain


# 2. 将 RAG链条 组装进Agent里
def create_agent_with_memory():
    # LLm
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ('system','你是一个强大的助手。你能查天气，也能查《战争与和平》。请尽力回答用户所提的所有问题。'),
        MessagesPlaceholder(variable_name="history"), # 05篇所学:记忆占位符
        ('human','{input}'),
        MessagesPlaceholder(variable_name="agent_scratchpad") # 05篇所学:ReAct 思考链，使其能够调用工具
    ])

    # Tool
    rag_chain_instance = build_rag_chain(llm_instance=llm)


    @tool
    def search_war_and_peace(query):
        """查询《战争与和平》小说中的内容，包括人物、情节、历史事件等"""
        print(f'\n正在检索《战争与和平》:{query}')
        return rag_chain_instance.invoke(query)

    @tool
    def get_weather(location):
        """模拟获得天气信息"""
        return f"{location}当前天气：23℃，晴，风力2级"

    tools = [get_weather,search_war_and_peace]

    # 创建Agent
    agent = create_tool_calling_agent(llm=llm,tools=tools,prompt=prompt)
    agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=False)

    # 封装Memory
    store = {}

    def get_session_history(session_id:int):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]


    # 添加记忆功能
    agent_with_memory = RunnableWithMessageHistory(
        runnable=agent_executor,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    return agent_with_memory


# 测试

if __name__ == '__main__':
    session_id = 'user123'
    agent = create_agent_with_memory()
    while 1:
        user_input = input('\n你:')
        if user_input=='quit':
            print('拜拜~')
            exit()
        response = agent.invoke(
            {'input':user_input},
            config={'configurable':{'session_id':session_id}}
        )
        print(f"AI:{response['output']}")
























