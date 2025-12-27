from agents.mcp import MCPServerStdio, MCPServerStdioParams
from openai import AsyncOpenAI
from agents.agent import Agent
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from m12_agents_sdk_swarm.tools import execute_refund, check_seat
from config import AMAP_MAPS_API_KEY,OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url="https://api.deepseek.com")
model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=client)

# 创建 Server，传入 params
amap_server = [
    MCPServerStdio(
        name="amap",
        params=MCPServerStdioParams(
            command="npx",
            args=["-y", "@amap/amap-maps-mcp-server"],
            env={"AMAP_MAPS_API_KEY": AMAP_MAPS_API_KEY}
        )
    )
]

# === 1. 创建所有Agent ===

# 退票专员
refund_agent = Agent(
    name="RefundAgent",
    instructions=lambda context, __: f"""你是退票专员。

【客户信息】
- 姓名: {context.context.get('user_name')}
- 航班号: {context.context.get('flight_no')}

【核心职责】
1. 当用户表达退票意图时，立即调用 execute_refund 工具完成退票
2. 不要问用户是否确认，直接执行
3. 执行完工具后，告知用户退款状态

【转接规则】
- 如果用户改变主意想改签，转接到 ChangeAgent
- 如果用户询问其他问题，转接到 TriageAgent
- 退票完成后，询问用户是否还需要其他帮助

【重要】你已经被转接过来，说明用户想退票，直接执行工具即可，不要犹豫！
""",
    tools=[execute_refund],
    model=model
)

# 改签专员
change_agent = Agent(
    name="ChangeAgent",
    instructions=lambda context, __: f"""你是改签专员。

【客户信息】
- 姓名: {context.context.get('user_name')}
- 航班号: {context.context.get('flight_no')}

【核心职责】
1. 当用户表达改签意图时，立即调用 check_seat 工具查询座位
2. 不要问用户是否确认，直接执行
3. 执行完工具后，告知用户结果

【转接规则】
- 如果用户改变主意想退票，转接到 RefundAgent
- 如果用户询问其他问题，转接到 TriageAgent
- 改签完成后，询问用户是否还需要其他帮助

【重要】你已经被转接过来，说明用户想改签，直接执行工具即可！
""",
    tools=[check_seat],
    model=model,
)

# 前台分诊员(动态提示词)
triage_agent = Agent(
    name="TriageAgent",
    instructions=lambda context, __: f"""你是航空公司前台客服。

【客户信息】
- 姓名: {context.context.get('user_name')}
- 航班号: {context.context.get('flight_no')}

【转接规则】
1. 用户说"退票"、"退款"、"取消航班" → 转接到 RefundAgent
2. 用户说"改签"、"换航班"、"改时间" → 转接到 ChangeAgent
3. 用户想查询某个附近地方的酒店、景点信息时 → 调用 amap_server
4. 其他问题由你自己回答

【重要】
- 转接时要明确告知用户："我帮您转接到XX专员"
- 不要重复询问用户意图，识别后立即转接
""",
    mcp_servers=amap_server,
    model=model,
)

# === 2. 建立 Handoff 网络 ===

# 前台可转给两位专员
triage_agent.handoffs = [refund_agent, change_agent]

# 专员之间也可互相转接，并能回退到前台
refund_agent.handoffs = [change_agent, triage_agent]
change_agent.handoffs = [refund_agent, triage_agent]