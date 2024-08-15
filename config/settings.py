from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# 基本配置参数
MAX_AGENTS: int = 100
MEMORY_LIMIT: int = 1000

# 高级功能配置
USE_MESSAGE_QUEUE: bool = False
USE_DATA_PERSISTENCE: bool = False
USE_HEALTH_CHECK: bool = False
USE_DISTRIBUTED_LOCK: bool = False

# 消息队列配置
MESSAGE_QUEUE_CONFIG: Dict[str, Any] = {
    "host": "localhost",
    "port": 5672,
    "virtual_host": "/",
    "username": "guest",
    "password": "guest",
    "heartbeat": 600,
    "blocked_connection_timeout": 300,
}

# 数据持久化配置
DATABASE_CONFIG: Dict[str, Any] = {
    "url": "postgresql://user:password@localhost/dbname",
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}

# 健康检查配置
HEALTH_CHECK_CONFIG: Dict[str, Any] = {
    "interval": 60,  # 秒
    "timeout": 10,  # 秒
    "failure_threshold": 3,
    "success_threshold": 1,
}

# 分布式锁配置
DISTRIBUTED_LOCK_CONFIG: Dict[str, Any] = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": None,
    "socket_timeout": 10,
    "lock_timeout": 10,
}

# Agent配置
AGENT_CONFIG: Dict[str, Any] = {
    "max_memory": 1000,
    "max_tasks": 10,
    "task_timeout": 300,
}

# 日志配置
LOG_DIR = "logs"
SERVICE_NAME = "HighAvailabilityAgentFramework"

# Vision Model配置
VISION_MODEL_CONFIG = {
    "api_key": os.getenv("AZURE_API_KEY"),
    "base_url": os.getenv("AZURE_BASE_URL"),
    "api_version": os.getenv("AZURE_API_VERSION"),
    "deploy_name": os.getenv("AZURE_DEPLOY_NAME"),
}

# 定义截图保存路径
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")

# 确保目录存在
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# LLM配置
LLM_CONFIG = {
    "default_provider": "gpt",  # 默认使用的LLM提供者
    "providers": {
        "gpt": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-4-1106-preview",
        },
        "claude": {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "model": "claude-2",
        },
        "deepseek": {
            "api_key": os.getenv("DEEPSEEK_API_KEY"),
            "model": "deepseek-chat",
        },
    },
}
