# 🧩 模块说明：LangGraph 基础篇 - 从状态机到智能 Agent

> 📌 核心知识点：StateGraph 基础结构｜MessagesState 对话状态｜ToolNode 工具执行｜条件路由｜MemorySaver 记忆｜System Prompt 无污染注入｜LangSmith 追踪

---

### 1. `state_node_edge.py` （LangGraph 最小状态机）

演示 LangGraph 最基础的三要素：State（状态）、Node（节点）、Edge（边）。

- ✅ 掌握点：
  - 定义 `TypedDict` 作为状态（如 `{"count": int}`）。
  - 编写节点函数（`node_a`, `node_b`）处理状态并返回更新。
  - 使用 `add_edge(START, "A")`、`add_edge("A", "B")` 构建线性流程。
  - 调用 `app.get_graph().draw_mermaid_png()` 生成可视化流程图。

- 输出：
  - 控制台打印状态变化过程。
  - 生成 `workflow.png` 流程图。

> 💡 此脚本**不涉及 LLM 或对话**，仅用于理解 LangGraph 底层机制。

---

### 2. `workflow.png` （状态机流程图）

由 `state_node_edge.py` 自动生成的 Mermaid 可视化图。

- 内容：
  - 展示 `START → A → B → END` 的线性执行流。
  - 节点 `A` 和 `B` 各将 `count` 加 1。
- 作用：
  - 直观理解 LangGraph 的“图”本质。
  - 为后续复杂控制流（如循环、分支）打下认知基础。

---

### 3. `langsmith_trace.py` （状态机 + LangSmith 追踪）

在 `1.` 的基础上启用 LangSmith，实现执行过程可视化追踪。

- ✅ 掌握点：
  - 设置环境变量：`LANGCHAIN_TRACING_V2=true`、`LANGCHAIN_PROJECT="my_demo"`。
  - 无需修改节点逻辑，自动上报每一步状态变更。
  - 在 [LangSmith UI](https://smith.langchain.com) 查看执行轨迹。

- 注意：
  - 仍是一个**纯状态机示例**（count +1 +1），**非对话 Agent**。
  - 用于验证 LangSmith 集成是否生效。

---

### 4. `conditional_router.py` （首个 ReAct Agent：无记忆）

构建第一个真正意义上的 LangGraph Agent：支持工具调用与条件循环。

- ✅ 掌握点：
  - 使用 `MessagesState` 管理对话历史。
  - 定义 `@tool def get_weather(location)` 并绑定到 LLM。
  - 实现 `should_continue` 函数判断是否需调用工具。
  - 构建 `agent → (条件) → tools → agent` 的 ReAct 循环。
  - 通过 `app.invoke({"messages": [...]})` 触发执行。

- 效果：
  - 输入“北京天气如何？” → 调用工具 → 返回天气。
  - 输入“你好” → 直接回答，不触发工具。
- 局限：
  - **无记忆**：每次 `invoke` 都是独立会话。

---

### 5. `agent_with_memory.py` （完整 Agent：带记忆 + 系统提示）

在 `4.` 基础上升级为生产级 Agent 范式。

- ✅ 掌握点：
  - 启用 `MemorySaver()` 实现跨轮次记忆（`checkpointer=MemorySaver()`）。
  - 通过 `config={"configurable": {"thread_id": "user123"}}` 绑定会话。
  - 在 `call_model` 中动态注入 `SystemMessage(content=sys_prompt)`，**但不写入 state**，避免污染历史。
  - 保留 LangSmith 追踪能力。

- 效果：
  - 支持连续对话（如“查北京天气” → “那上海呢？”）。
  - 系统指令始终生效，但不会出现在消息历史中。
  - 全流程可追踪、可调试。

---

### 🔔 全局注意事项

- **学习路径建议**：  
  `1.`（理解图） → `3.`（理解追踪） → `4.`（理解 ReAct） → `5.`（理解记忆+prompt）
- 所有 `.py` 文件均依赖 `.env` 中的 `OPENAI_API_KEY` 和 `LANGCHAIN_API_KEY`。
- 若想复用你的 RAG 工具，只需将 `get_weather` 替换为 `search_war_and_peace`，其余逻辑不变。
- `workflow.png` 仅反映 `state_node_edge.py` 的简单线性流，**不代表 Agent 结构**。

---

### 💡 **建议**
- 尝试扩展 `agent_with_memory.py`，添加更多自定义工具（如RAG检索工具）
- 实验不同的条件路由逻辑，实现更复杂的Agent决策路径
- 使用LangSmith深入分析和优化Agent的推理过程
- 尝试实现多Agent协作系统，通过LangGraph连接多个专业化Agent