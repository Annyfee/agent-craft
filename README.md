# 💻 Agent Craft

> 智能体开发教学库 | A beginner-friendly guide to building AI agents


🔥 从零开始上手agent智能体，掌握langchain、rag、prompt、langgraph等核心技术栈

本仓库专注于 AI Agent 开发的学习与实践，通过系统化的案例和详细的代码注释，帮助开发者快速掌握从基础LLM调用到复杂Agent构建的完整技能栈。

💡 项目将持续更新，目标是构建一个系统、实用的 AI Agent 学习案例库。

📘 本仓库开箱即用，仅需配置 API_KEY。

✍️ 代码可与博客配套使用，博客会重点讲解Agent知识构建与流程解析。

博客同步发布：

👉 [我的CSDN主页](https://blog.csdn.net/2401_87328929)

👉 [CSDN对应专栏](https://blog.csdn.net/2401_87328929/category_12970267.html)

🙋‍♂️ 技术交流 / 更新 / 答疑：微信 **a19731567148**（备注 GitHub）

---
## 🚅 目录跳转

| 仓库                                                | 博客                                             | 技术栈              | 知识点                  | 难度 |
|---------------------------------------------------|------------------------------------------------|------------------|----------------------|-----|
| [01 Agent 入门 & 快速运行](01%20Agent%20入门%20&%20环境搭建/) | [🏠](01%20Agent%20入门%20&%20环境搭建/Agent-demo.py) | 基础LLM            | Agent概念              | ⭐ |
| [02 LLM基础与调用](02%20LLM基础与调用/1.%20llm基础调用.py)      | [🏠](02%20LLM基础与调用/1.%20llm基础调用.py)            | LLM/API调用/Prompt | 调用模型接口、初识prompt、多轮对话 | ⭐ |


---

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
---

## 📚 学习路径

### 🎯 第一章：Agent 入门 & 快速运行
- **核心技能**: 运行Agent-demo
- **学习目标**: 了解Agent是什么，怎么用
- **技术要点**: 环境配置

### 🎯 第二章：LLM基础与调用
- **核心技能**: 多轮对话Agent构建
- **学习目标**: 实现智能对话系统
- **技术要点**: 对话历史、上下文管理、角色设定

## 🤝 贡献指南
欢迎贡献代码 / 提交 Issue / Pull Request
- Fork 仓库  
- 创建分支进行修改  
- 提交 PR 并描述修改内容
