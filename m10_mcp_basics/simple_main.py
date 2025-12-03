import asyncio
import os
from m10_mcp_basics.simple_client import SimpleClient
from config import AMAP_MAPS_API_KEY

# 复制当前py进程的环境变量,并在复制的环境变量里新增一条，确保安全可控
env_vars = os.environ.copy()
env_vars["AMAP_MAPS_API_KEY"] = AMAP_MAPS_API_KEY

async def main():
    print('🔥 正在进行单次调用...')
    client = SimpleClient(
        command="npx",
        args=["-y","@amap/amap-maps-mcp-server",AMAP_MAPS_API_KEY],
        env=env_vars
    )

    # 这一步会经历:启动进程 - 握手 - 调用 - 杀进程
    result = await client.run_once("maps_text_search", {"keywords": "北京大学"})
    print(f'✅️ 结果:{result[:300]}')


if __name__ == "__main__":
    asyncio.run(main())