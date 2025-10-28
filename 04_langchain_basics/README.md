## 🧩 模块说明：LangChain 基础核心组件

📌 **核心知识点**：  
LLM 调用｜Prompt 设计｜Chain 构建｜Memory 记忆｜实战练习

---

### 1. `01_Models.py`（模型调用）  
封装 LLM 实例，实现标准调用流程。  

✅ 掌握点：  
- 如何初始化 ChatOpenAI 或 DeepSeek  
- 设置 API Key 和 base_url

---

### 2. `02_Prompt.py`（提示词构建）  
使用 `ChatPromptTemplate` 构建可复用的 Prompt 模板。  

✅ 掌握点：  
- 系统提示 + 历史消息 + 用户输入  
- 使用 `{input}` 占位符  
- 多轮对话的基础结构

---

### 3. `03_Chain.py`（链式调用）  
将 Prompt + LLM + Parser 组合成 Chain。  

✅ 掌握点：  
- 使用 `|` 操作符连接组件  
- 创建可复用的处理流程  
- 输出解析为字符串

---

### 4. `04_Memory.py`（记忆功能）  
添加会话记忆，实现多轮对话。  

✅ 掌握点：  
- 使用 `ChatMessageHistory` 存储历史  
- `RunnableWithMessageHistory` 包装 Chain  
- 保持上下文连贯性

---

### 5. `05_practice.py`（综合实践）  
整合所有组件，搭建一个带记忆的 AI 对话机器人。  

✅ 掌握点：  
- 完整流程串联  
- 实际运行体验  
- 可直接扩展为 Web 应用

💡 建议：跑通后，试试让 AI 记住你喜欢的颜色，并在后续对话中提及。