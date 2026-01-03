# 修改导入方式以使用正确的openai-agents包
from agents.tool import function_tool

# 全局上下文，所有 Agent 共享
context_variables = {
    "user_name":"张三(白金会员)",
    "flight_no":"CA1234"
}

# 业务工具
@function_tool
def execute_refund():
    """执行退款逻辑"""
    return "✅️ 退款申请已提交，预计3个工作日内到账。"

@function_tool
def check_seat():
    """查询座位余量"""
    return "✅ 明日航班尚有余票。"