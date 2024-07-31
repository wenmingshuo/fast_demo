import asyncio
import sys
from fastapi import FastAPI
import uvicorn
from tortoise import Tortoise
from uvicorn.config import LOGGING_CONFIG
from apps.admin.views import AdminRouter
from tortoise.contrib.fastapi import register_tortoise

from middlewares import middleware_init

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

app = FastAPI()
app.include_router(AdminRouter, prefix=f'/admin', tags=['后台'])
# 初始化中间件
middleware_init(app)
TORTOISE_ORM = {
    "connections": {
        "default": 'mysql://root:root@127.0.0.1:3306/wen_oms'
    },
    "apps": {
        "models": {
            "models": ["apps.admin.models"],
            "default_connection": "default"
        }
    },
    "use_tz": True,  # 确保使用时区
    "timezone": "Asia/Shanghai"  # 设置默认时区
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
)

if __name__ == '__main__':
    # 运行初始化函数
    custom_logging_config = LOGGING_CONFIG
    custom_logging_config['formatters']['access']['fmt'] = '%(asctime)s - %(levelname)s - %(message)s'
    custom_logging_config['formatters']['default']['fmt'] = '%(asctime)s - %(levelname)s - %(message)s'
    uvicorn.run(
        'main:app', host='0.0.0.0', port=10010,
        env_file='.env', reload=True, log_config=custom_logging_config
    )
