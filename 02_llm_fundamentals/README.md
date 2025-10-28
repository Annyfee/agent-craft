## 🧩 模块说明：LLM 调用与多轮对话 Agent

📌 **核心知识点**：  
LLM 调用｜Prompt 编写与设计｜多轮对话记忆｜独立搭建智能体

---

### 1. `01_basic_llm_invocation`（LLM 模型调用）  
使用 DeepSeek 官方推荐的调用方式，  
这是后续所有 API 调用的通用结构，可直接复用。  

✅ 掌握点：  
- 如何初始化 LLM 实例  
- 标准的 API 调用格式  
- 快速切换模型和参数

---

### 2. `02_conversational_agent`（多轮问答 Agent）  
整合了 LLM + Prompt + Memory，实现有记忆的对话。  

🔧 使用提示：  
想换 AI 人设或初始提问？  
👉 直接修改 `messages` 中的 `content` 即可。

✅ 掌握点：  
- 多轮对话如何保持上下文  
- Prompt 结构设计  
- 记忆模块（Memory）的基本用法