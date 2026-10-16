# 本地代码查询：带认证的 HTTP MCP

本例复用 `s03_parallel_search.py` 的官方 LangChain MCP 适配器，展示另一种
场景：连接本机的代码索引服务，发现工具，再直接调用 `sem_find` 查询函数源码
及相关实体。无需模型 API Key，不使用 `.env`，不运行 Agent 推理。

## 1. 启动 Sem HTTP 预览版

**Sem 0.27.0 发布版尚不支持此 HTTP 接口**。接口已通过
[Sem PR #518](https://github.com/Ataraxy-Labs/sem/pull/518) 合并到主分支；
请构建提交 `2e6a47fcd35ce269eec702dd3532341dba52902b` 或之后的兼容版本。
按 [Sem HTTP 指南](https://github.com/Ataraxy-Labs/sem/blob/2e6a47fcd35ce269eec702dd3532341dba52902b/docs/mcp-http.md)
启动服务。配置显式 `SEM_REPO`（可信 Git 仓库的绝对路径）、随机
`SEM_MCP_HTTP_TOKEN`，监听 `127.0.0.1:8765`。

服务器和此客户端应运行在同一台机器。云平台中的 localhost 不代表你的电脑。
不要把此预览服务直接暴露到公网，也不要提交 token 到 Git。

## 2. 安装已有的最小依赖并查询

在仓库根目录运行（建议使用独立虚拟环境）：

```sh
pip install -r m11_mcp_advanced/requirements-parallel.txt
python -m m11_mcp_advanced.s04_sem_code parse_config
```

客户端终端须设置与服务器相同的 `SEM_MCP_HTTP_TOKEN`。将 `parse_config`
替换为目标仓库中的实际实体名。结果保留适配器的内容块；找不到实体会返回工具错误。

## 与网页搜索例子的区别

- 请求访问本地仓库，而不是公共网页；使用 Authorization 请求头认证。
- 查询实体名称，返回源码上下文，预算为 1200 tokens；不调用外部模型。
- HTTP 端只开放 `sem_find`、`sem_grep`；不执行编辑、构建、检查命令或合并。
- 索引会写缓存，因此只读指不修改源代码，不代表完全不写磁盘。
- 服务器不是多租户沙箱；仅对可信客户端开放。停止服务即可撤销连接。
