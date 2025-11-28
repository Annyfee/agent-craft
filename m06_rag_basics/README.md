## 🧩 模块说明：RAG 基础 - 构建专属知识库

📌 **核心知识点**：  
RAG 概念｜文本加载与分块 (Load & Split)｜向量化 (Embedding)｜向量存储 (FAISS)｜LCEL RAG 链

---

### 1. `load_and_split.py`（文本加载与分块）
加载本地 `.txt` 文档，并使用 `RecursiveCharacterTextSplitter` 将其智能分割成“知识卡片”。

✅ **掌握点**：
- 使用 `TextLoader` 将文件加载为 `Document` 对象。
- **RAG 核心**：深入理解 `chunk_size` (分块大小) 和 `chunk_overlap` (重叠) 的调优策略。
- `RecursiveCharacterTextSplitter` 如何按 `["\n\n", "\n", " "]` 优先级智能分割。

---

### 2. 文本向量化功能
项目使用根目录下的 `embeddings.py` 模块提供文本向量化功能，该模块封装了 `HuggingFaceEmbeddings`，支持自动下载和加载本地 Embedding 模型。

✅ **掌握点**：
- 通过 `get_embeddings()` 函数获取向量化模型，默认使用 `BAAI/bge-small-zh-v1.5`。
- 函数会自动下载模型到本地 `models` 目录，之后可离线使用。
- 理解 Embedding（向量化）是 RAG 的"语义标签"，用于实现"语义搜索"。

---

### 3. `build_index.py`（向量存储与索引构建）
使用 FAISS 向量索引库将向量化后的文本片段构建为可检索的向量数据库，并持久化到本地。

✅ **掌握点**：
- 使用 `FAISS.from_documents` 构建向量索引库。
- 通过 `save_local` 方法将向量索引持久化到本地文件系统（保存为"faiss_index"目录）。
- 实现文本的完整处理流程：加载 -> 分割 -> 向量化 -> 索引构建 -> 持久化。

---

### 4. `rag_chain_full.py`（LCEL 完整 RAG 链）
使用 LCEL（LangChain 表达式语言）“手动组装”一个完整的 RAG 流程，实现“检索-增强-生成”的闭环。

✅ **掌握点**：
- R (Retrieval): `db.as_retriever()` 如何作为检索器。
- A (Augmented): `ChatPromptTemplate` 如何接收 `{context}` 和 `{question}`。
- G (Generation): LLM 如何根据上下文（Context）回答问题。
- **LCEL 核心**：使用 `{"context": ..., "question": RunnablePassthrough()}` 并行组装数据流。
- 使用 `format_docs` 函数将 `List[Document]` 适配为 `str` 字符串。

---

💡 **建议**：
跑通所有示例后，尝试用你自己的 `.txt` 文件替换项目中的 `knowledge_base.txt`，并调整 `chunk_size` 参数，观察分块结果和 RAG 问答效果的变化。