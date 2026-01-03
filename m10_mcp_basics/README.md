# 🧩 模块说明：MCP 基础篇 - 构建多模态协作协议服务器

> 📌 核心知识点：MCP协议原理｜FastMCP框架使用｜Stdio通信｜Streamable HTTP服务｜工具定义与注册

---

### 1. `s01_stdio_server.py` （标准输入输出MCP服务器）

实现基于标准输入输出的MCP服务器，支持本地进程间通信。

- ✅ 掌握点：
  - 使用FastMCP创建MCP服务实例
  - 定义和注册工具函数
  - 异步工具函数的实现方式
  - Stdio通信模式的配置与运行

- 功能：
  - 创建名为"WeatherService"的MCP服务器
  - 提供`get_weather`工具，模拟查询指定城市天气
  - 支持异步调用，FastMCP自动处理协程
  - 采用标准输入输出作为通信通道

> 💡 这种模式适合本地进程间通信，程序启动后会等待客户端指令，无默认输出。

---

### 2. `s02_streamable_http_server.py` （HTTP协议MCP服务器）

实现基于HTTP协议的MCP服务器，支持远程网络调用。

- ✅ 掌握点：
  - FastMCP服务器的网络配置
  - HTTP通信模式的实现
  - 监听地址和端口的设置
  - Streamable HTTP运行模式的使用

- 功能：
  - 创建名为"WeatherService"的网络MCP服务器
  - 配置监听地址(0.0.0.0)和端口(8001)
  - 提供与stdio_server相同的`get_weather`工具
  - 自动启动uvicorn服务器，支持远程调用

> 💡 这种模式适合构建可远程访问的MCP服务，便于分布式系统集成。

---

### 🔔 全局注意事项

- **学习路径建议**：
  `1.`（stdio_server） → `2.`（streamable_http_server）
- 两个文件均实现了相同的天气查询服务，仅通信方式不同
- Stdio模式下，服务器启动后无输出，需通过MCP客户端连接
- HTTP模式下，服务器启动后会监听指定端口，可通过网络访问

---

### 💡 **扩展建议**
- 尝试添加更多工具函数，扩展服务能力
- 集成真实的天气API，替代模拟数据
- 探索FastMCP的其他配置选项和功能
- 结合m11_mcp_advanced中的客户端实现，构建完整的MCP应用