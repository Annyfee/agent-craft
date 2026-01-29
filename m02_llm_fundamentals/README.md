## 🧩 模块说明：LLM 调用与多轮对话 Agent

📌 **核心知识点**：  
LLM 调用｜Prompt 编写与设计｜多轮对话记忆｜独立搭建智能体

---

### 1. `s01_basic_llm_invocation`（LLM 模型调用）  
使用 DeepSeek 官方推荐的调用方式，  
这是后续所有 API 调用的通用结构，可直接复用。  

✅ 掌握点：  
- 如何初始化 LLM 实例  
- 标准的 API 调用格式  
- 快速切换模型和参数

---

### 2. `s02_conversational_agent`（多轮问答 Agent）  
整合了 LLM + Prompt + Memory，实现有记忆的对话。  

🔧 使用提示：  
想换 AI 人设或初始提问？  
👉 直接修改 `messages` 中的 `content` 即可。

✅ 掌握点：  
- 多轮对话如何保持上下文  
- Prompt 结构设计  
- 记忆模块（Memory）的基本用法

---

### 3. `s03_llm_temperature`（温度参数对输出的影响）  
演示不同 temperature 参数对 LLM 输出多样性和创造性的影响。  

🔧 使用提示：  
想测试不同温度参数的效果？  
👉 直接修改代码中的 `temperature` 值即可（范围通常为 0-2）。

✅ 掌握点：  
- temperature 参数的作用和影响  
- 如何根据场景选择合适的温度值  
- 低温度（稳定）与高温度（随机）输出的对比