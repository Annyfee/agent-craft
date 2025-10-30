## 🧩 模块说明：LangChain Agents 进阶核心组件

📌 **核心知识点**：  
Function Calling｜@tool 工具封装｜ReAct 循环｜Agent 构建｜SQL Agent｜记忆+流式｜开发优化

---

### 1. `01_define_toolbox.py`（工具函数定义）  
使用 `@tool` 装饰器将 Python 函数封装为 LangChain 可调用的工具。  

✅ 掌握点：  
- 如何用 `@tool` 定义工具  
- 必须添加三引号描述（作为提示词）  
- 支持任意自定义逻辑函数

---

### 2. `02_general_agent.py`（通用 Agent 构建）  
基于 `create_tool_calling_agent` 创建支持工具调用的智能体。  

✅ 掌握点：  
- ReAct 思维循环：思考 → 行动 → 观察 → 再思考  
- 使用 `MessagesPlaceholder("agent_scratchpad")` 记录推理过程  
- `AgentExecutor` 执行完整流程，支持 `verbose=True` 查看思考链

---

### 3. `03_sql_agent.py`（SQL 专用 Agent）  
一键构建自然语言查询数据库的智能体。  

✅ 掌握点：  
- 使用 `create_sql_agent` 快速接入 SQLite 数据库  
- 自动分析表结构、生成 SQL 并执行  
- 无需手动定义工具，开箱即用

---

### 4. `04_memory_general_agent.py`（带记忆的 Agent）  
将 Agent 与对话历史结合，实现多轮上下文感知。  

✅ 掌握点：  
- 在 Prompt 中加入 `MessagesPlaceholder("history")`  
- 使用 `RunnableWithMessageHistory` 包装 AgentExecutor  
- 实现“记住用户身份”、“持续追问”的真实对话体验

---

### 5. `05_caching.py`（缓存优化技巧）  
在开发调试阶段避免重复调用 LLM，节省成本与时间。  

✅ 掌握点：  
- 使用 `set_llm_cache(InMemoryCache())` 启用缓存  
- 第一次调用远程请求，后续命中缓存秒出结果  
- 开发时开启，上线前关闭（仅用于测试）

---

### 6. `06_streaming.py`（流式输出实战）  
实现 AI 回复像打字机一样逐字输出，提升用户体验。  

✅ 掌握点：  
- 设置 `streaming=True` 启用流式模式  
- 添加 `callbacks=[StreamingStdOutCallbackHandler()]` 实时打印 token  
- 使用 `print("AI: ", end="", flush=True)` 确保提示立即显示

---

💡 建议：  
跑通所有示例后，尝试将 `get_weather` 和 `query_user_info` 组合进一个带记忆的 Agent，让 AI 能连续问：“你是谁？”、“北京天气怎么样？”、“你喜欢什么颜色？”，并记住你的回答。