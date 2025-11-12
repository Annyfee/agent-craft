# 🤖 Agent Craft

> 智能体开发教学库 | A beginner-friendly guide to building AI agents

[![Python CI](https://github.com/Annyfee/agent-craft/actions/workflows/ci.yml/badge.svg)](https://github.com/Annyfee/agent-craft/actions/workflows/ci.yml)

## 📘 项目简介

**Agent Craft** 是一个系统性开源教学项目，采用 **「博客讲解 + 代码实践」双驱动模式**，带你从零构建完整的 AI Agent 开发能力。

- 📄 **配套博客详解**：每章内容均配有 CSDN
  深度文章，涵盖原理剖析、代码解析与调试技巧
- 💻 **可运行代码仓库**：每个模块对应独立目录，含完整代码、详细注释与运行指引，支持本地复现
- 🚀 内容覆盖：从 **Prompt 工程** 到 **LangChain / LangGraph / RAG / SDK 封装**
- ⚙️ 能力进阶：涵盖 **智能体思维链、工具调用、任务规划、多智能体协作**

> 💡 本仓库目标：帮助开发者从零构建可运行的智能体应用，真正理解 Agent 的底层逻辑，而不仅仅是“调用框架”。

---

## 🧭 模块总览（16 模块）

> 💡 每个模块对应独立目录（含代码、说明与示例），可独立运行与学习。  
> 🔥 已更新至 07 Rag 进阶篇，持续更新中！

|     章节      | 模块                                                                                                      |                                 博客                                  | 核心关键词                                               |  难度   |
|:-----------:|:--------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------:|:----------------------------------------------------|:-----:|
| 🏗️ **基础篇** | [01 Agent 入门 & 环境搭建](https://github.com/Annyfee/agent-craft/tree/main/01_agent_introduction)            | [🏠](https://blog.csdn.net/2401_87328929/article/details/153729555) | OpenAI API                                          |   ⭐   |
|             | [02 LLM 基础调用](https://github.com/Annyfee/agent-craft/tree/main/02_llm_fundamentals)                     | [🏠](https://blog.csdn.net/2401_87328929/article/details/153735431) | LLM API 调用 · prompt · 上下文记忆                         |   ⭐   |
|             | [03 Function Calling 与工具调用](https://github.com/Annyfee/agent-craft/tree/main/03_function_calling_tools) | [🏠](https://blog.csdn.net/2401_87328929/article/details/153866573) | Function Call · 工具函数封装                              |  ⭐⭐   |
| ⚙️ **框架篇**  | [04 LangChain 基础篇](https://github.com/Annyfee/agent-craft/tree/main/04_langchain_basics)                | [🏠](https://blog.csdn.net/2401_87328929/article/details/153978186) | LLM · Prompt · Chain · Memory                       |  ⭐⭐   |
|             | [05 LangChain 进阶篇](https://github.com/Annyfee/agent-craft/tree/main/05_langchain_advanced)              | [🏠](https://blog.csdn.net/2401_87328929/article/details/154064397) | Agents · 缓存 · 流式输出                                  |  ⭐⭐⭐  |
|             | [06 RAG 基础篇](https://github.com/Annyfee/agent-craft/tree/main/06_rag_basics)                            | [🏠](https://blog.csdn.net/2401_87328929/article/details/154230067) | RAG概念 · Split · Embedding · FAISS · RAG 链           |  ⭐⭐   |
|             | [07 RAG 进阶篇](https://github.com/Annyfee/agent-craft/tree/main/07_rag_advanced)                          | [🏠](https://blog.csdn.net/2401_87328929/article/details/154408744) | Chroma · Reranker · RAG工具化 · 集成                     |  ⭐⭐⭐  |
|             | 08 LangGraph 基础篇                                                                                        |                                🚧撰写中                                | `State` · `Node` · `Conditional Edge` · RAG+反思      |  ⭐⭐⭐  |
|             | 09 LangGraph 进阶篇                                                                                        |                                 🚧                                  | `Multi-Agent` · `Human-in-the-Loop` · “总控-员工”架构     | ⭐⭐⭐⭐  |
| 🧠 **智能篇**  | 10 MCP 基础 (Client)                                                                                      |                                 🚧                                  | `MCP` 协议 · `CherryStudio` · 消费公共 MCP                |  ⭐⭐⭐  |
|             | 11 MCP 进阶 (Server)                                                                                      |                                 🚧                                  | `Streamable HTTP` · `src layout` · 构建私有 MCP         | ⭐⭐⭐⭐  |
|             | 12 Swarm & Agents SDK                                                                                   |                                 🚧                                  | `Swarm` · `Handoff` · “航空公司客服”项目                    | ⭐⭐⭐⭐  |
| 🏁 **实战篇**  | 13 Streamlit 快速入门                                                                                       |                                 🚧                                  | `st.chat_input` · `st.session_state` · 封装 RAG Agent |  ⭐⭐⭐  |
|             | 14 综合实战项目                                                                                               |                                 🚧                                  | LangGraph + RAG + MCP + Streamlit + Vercel          | ⭐⭐⭐⭐⭐ |
| 🚀 **工程篇**  | 15 部署与本地化                                                                                               |                                 🚧                                  | `Ollama` · `LM Studio` · `LangServe`                |  ⭐⭐⭐  |
|             | **16 项目打包与发布**                                                                                          |                                 🚧                                  | `pyproject.toml` · `pip build` · `setuptools` · 发布  | ⭐⭐⭐⭐  |

---

## 🧩 当前学习建议（适用于已完成模块）

目前已开放模块：**01 ~ 07**。  
建议按顺序学习，每一章都有完整代码示例与注释。

### ✅ 模块 01 — Agent 入门 & 环境搭建

- **目标**：理解 Agent 概念，完成环境配置与首次调用。
- **内容**：环境依赖｜API Key 配置｜最小可运行 Agent

### ✅ 模块 02 — LLM 基础调用

- **目标**：掌握模型调用逻辑，初步构建智能体能力。
- **内容**：LLM了解与调用｜Prompt编写与逻辑构思｜多轮对话记忆｜独立搭建一个智能体

### ✅ 模块 03 — Function Calling 与工具调用

- **目标**：实现 LLM 调用外部函数，赋予模型“执行力”。
- **内容**：Function calling原理｜工具函数封装｜API接入实践｜多轮调用流程｜Agent能力扩展

### ✅ 模块 04 — LangChain 基础篇

- **目标**：认识Langchain六大模块，学会用Langchain构建智能体。
- **内容**：LLM 调用｜Prompt 设计｜Chain 构建｜Memory 记忆｜实战练习

### ✅ 模块 05 — LangChain 进阶篇

- **目标**：掌握Langchain Agents的核心机制，构建能调用工具、持续思考、具备记忆的智能体。
- **内容**：Function Calling｜@tool 工具封装｜ReAct 循环｜Agent 构建｜SQL Agent｜记忆+流式｜开发优化

### ✅ 模块 06 — Rag 基础篇

- **目标**：理解Rag的概念与整个运行流程，并能够搭建一个可以引用外部知识库获取信息的智能体。
- **内容**：RAG 概念｜文本加载与分块 (Load & Split)｜向量化 (Embedding)｜向量存储 (FAISS)｜LCEL RAG 链

### ✅ 模块 07 — Rag 进阶篇

- **目标**：学会进阶的Chroma向量数据库，会Reranker精排序，最终将04到07所学的Langchain六大模块完整集成。
- **内容**：Chroma 持久化 | Reranker 精排 | RAG 工具化 | Langchain六大模块集成

> 📌 后续模块将陆续开放（LangGraph、MCP、多智能体等）

---

## 🧠 Agent Craft 的核心学习路径

> “让每个人都能真正理解 Agent 的底层逻辑，而不仅仅是调用框架。”

我们采用 **渐进式构建** 的教学理念，从最基础的 Prompt 开始，逐步搭建完整的 AI Agent 能力栈：

```mermaid
flowchart LR
    A[Prompt 层] --> B[LLM 核心调用]
    B --> C[LangChain 工具链]
    C --> D[RAG 检索增强生成]
    D --> E[LangGraph 流程控制]
    E --> F[MCP 扩展能力]
    F --> G[多智能体协作与规划]
    G --> H[SDK 封装与部署]
```

## 🚀 快速开始

### 1️⃣ 环境准备

```bash
# 克隆项目
git clone https://github.com/Annyfee/agent-craft.git
cd agent-craft

# 安装依赖
pip install -r requirements.txt
```

### 2️⃣ API Key 配置

```bash
# 复制环境变量模板
cp .env.example .env
```

在 `.env` 文件中配置：

```env
OPENAI_API_KEY=your_deepseek_api_key_here
```

> 💡 **获取API Key**: 访问 [DeepSeek官网](https://platform.deepseek.com/) 注册并获取API Key

### 3️⃣ 运行示例

```bash
python "01 Agent 入门 & 环境搭建/Agent-demo.py"
```

### 4️⃣ 运行测试

项目已集成CI/CD流程，包含基本测试和代码检查。你可以通过以下方式运行测试：

```bash
# 直接运行测试脚本（推荐，不需要安装额外依赖）
python tests/test_basic.py

# 或者使用pytest（如果已安装）
python -m pytest tests/ -v
```

测试将检查项目目录结构完整性和基本模块导入情况，即使部分依赖未安装，也能完成基本检查。

---

## 🤝 参与和交流

欢迎提交 **Issue / PR / 改进建议**

如果有商业/技术交流需求，请联系我:

📬 微信：a19731567148（备注 Agent）

📖 个人博客：[CSDN 主页](https://blog.csdn.net/2401_87328929)

