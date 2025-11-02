## 🧩 模块说明：RAG 基础 - 构建专属知识库

📌 **核心知识点**：  
RAG 概念｜文本加载与分块 (Load & Split)｜向量化 (Embedding)｜向量存储 (FAISS)｜LCEL RAG 链

---

### 1. `01_load_and_split.py`（文本加载与分块）
加载本地 `.txt` 文档，并使用 `RecursiveCharacterTextSplitter` 将其智能分割成“知识卡片”。

✅ **掌握点**：
- 使用 `TextLoader` 将文件加载为 `Document` 对象。
- **RAG 核心**：深入理解 `chunk_size` (分块大小) 和 `chunk_overlap` (重叠) 的调优策略。
- `RecursiveCharacterTextSplitter` 如何按 `["\n\n", "\n", " "]` 优先级智能分割。

---

### 2. `02_embedding.py`（文本向量化）
演示如何加载本地 Embedding 模型，并将任意文本（知识卡片）转换为“语义向量”。

✅ **掌握点**：
- 使用 `HuggingFaceEmbeddings` 加载开源本地模型（如 `BAAI/bge-small-zh-v1.5`）。
- 理解 Embedding（向量化）是 RAG 的“语义标签”，用于实现“语义搜索”。
- 如何调用 `embed_query` 将文本转换为向量（一串数字）。

---

### 3. `03_build_index.py`（构建并存储索引）
整合“加载”、“分块”和“向量化”三个步骤，构建 FAISS 向量索引库，并将其**持久化**保存到本地磁盘。

✅ **掌握点**：
- 什么是 FAISS（轻量级、高性能的向量索引库）。
- 如何使用 `FAISS.from_documents` 一键完成“批量向量化+构建索引”。
- 如何使用 `db.save_local` 将索引保存到磁盘，实现**“离线索引”**。

---

### 4. `04_rag_chain_full.py`（LCEL 完整 RAG 链）
使用 LCEL（LangChain 表达式语言）“手动组装”一个完整的 RAG 流程，实现“检索-增强-生成”的闭环。

✅ **掌握点**：
- R (Retrieval): `db.as_retriever()` 如何作为检索器。
- A (Augmented): `ChatPromptTemplate` 如何接收 `{context}` 和 `{question}`。
- G (Generation): LLM 如何根据上下文（Context）回答问题。
- **LCEL 核心**：使用 `{"context": ..., "question": RunnablePassthrough()}` 并行组装数据流。
- 使用 `format_docs` 函数将 `List[Document]` 适配为 `str` 字符串。

---

💡 **建议**：
跑通所有示例后，尝试用你自己的 `.txt` 文件替换 `knowledge_base.txt`，并调整 `chunk_size` 参数，观察分块结果和 RAG 问答效果的变化。