import os
import pathlib
import logging
from datetime import datetime, timedelta
import asyncio 

# ---------- 以下是基础配置信息 ----------

# 调用本项目时使用的密码
PASSWORD = os.environ.get("PASSWORD", "123").strip('"') 

# 网页配置密码，设置后，在网页修改配置时使用 WEB_PASSWORD 而不是上面的 PASSWORD
WEB_PASSWORD = os.environ.get("WEB_PASSWORD", "67564534").strip('"') 

# API密钥
GEMINI_API_KEYS = os.environ.get("GEMINI_API_KEYS", "AIzaSyB8WZAjGkNvOsJbcnstmCRHZ7WyJ01r8TY,AIzaSyAXDoNlu9u5dFhbJhkqru9iZXTd2yYn5-8,AIzaSyAs9OfZmteNgOxy6L3AOQigZlzs8XAs8Jw,AIzaSyBkaiGeEnkive8WwvMAEAne-nbfI4H2vyY,AIzaSyDe2Viw5hlNTQM5gjQzl_mJqCMxFaSj3uA,AIzaSyCR2faMADtxo8Hx8zhx-7b2eaEsuZQTtvY,AIzaSyC7BsBAmQBZ8HsfqCjncYBwrwP5yiFXSRQ,AIzaSyDw-Rju2wboU3hwwpIHg45x5R-IvvU1x38,AIzaSyABlzNmp2RGAxxV5e13xs788ockChqSaTs,AIzaSyACXBpBeJVH5hKzjM2i9Q5iMXwuBaQHADw,AIzaSyDGETtwiz0HGTq8N2WBtyIplFM8qI2DvUY,AIzaSyDJnBIUWUvHx3BgJhWJF6i_f9U8hPB7MPs,AIzaSyB7HyFvYk6OCE9fMLQgAqGE86Vm2sndSdU,AIzaSyAZnSkEYTrHDllSnUJN5Z4X7Gk6LgolOlQ,AIzaSyBeKUxcOmpZhMJBsb6p35qZudj2ZrhCE-k,AIzaSyDXVEqcRws1t69t1WZRdgxA7wbCHuqHCXw,AIzaSyAZusyRzdrVBJpuI10f-8WE2WWKaeFh7X8,AIzaSyDEC9CGlCL6mJtHwJ8yCLKTSJ4tw0r0Bkw,AIzaSyC1U9RoDbO1ZKEGODAqmsq3xTymtDXIln8,AIzaSyC1gvzCnW-uXVrhgAz0avPxdEzDBZ84BhE,AIzaSyDg3bGQE2kRidsza75Jgqd1aLAx1fOkoJg,AIzaSyBycxkw4QcR0WfJii76jJMXqZ6LlbGcaEU,AIzaSyD-Nck_RoMaC2qc6PFVfaE7GTMNOe4y1D0,AIzaSyA-ruVqZupqv0qT8oRAWku9xnYbKfrLwkQ,AIzaSyAVKooPAg-S4MKcebFoSbaUNkVzDzFoIo4,AIzaSyDE3Ojsaf1T8iGqnd_kHchLjge31eUPoJ4,AIzaSyBeE75a3zINtAIwG4V1UL175aSjNb6pW9c,AIzaSyAlL3tlKO22DrIDkmqs9ScJWFNFwfN4QEI,AIzaSyBZdBawDf8ZPAKdxHtiywMsV5eHVGlL6Fo,AIzaSyDNuuj3YPSpdbsfExNJu0PJnz-PXDIQTrs,AIzaSyDt--WY2xGoqM_XNyNMTmq9t5Zqqq1t0tQ,AIzaSyCqD4Uxj9DjUuqg1ORz2ncZrfcZ9ZebdWw,AIzaSyDBUenFxYtpl_SH5XDBtbJqLPOH540B9xk,AIzaSyDbc_oT_gcii4LDK6fcqZ8NHNoDdKMOgOU,AIzaSyB7LOzoGW5DC3q-u6eupw14UoAh_3rZxQ0,AIzaSyDxawl15iofU9tXv-7SvRVENDlDEtaY5M4,AIzaSyArF3Fb8UHz3fYB8hhmRot1nXOZ7b7Og0M,AIzaSyApJqDcpJ6EeuM0149xP-UU0WtO76OWZrg,AIzaSyBd240-bXhtrSv2l7cU1ii5G8-DBQfS0HA,AIzaSyANug4zv8RMBBjyCOZHpMZmKaWTA71KJDw,AIzaSyB8mSPkJ-kxXTV3gf300C9YjkUceM5d2bM,AIzaSyAedrnoL7BXuKbOLZM-z6Ll-kLEeYZBQ28,AIzaSyBsX7XxZGj21wMc7Jz3TQ2jPORl3bEIrP8,AIzaSyDCfTx9vssaUE32lhgNwSMYqyzS5P2HghU,AIzaSyDrogC_c1_ettNZ2RVCDcbkVVN4pRndH4I,AIzaSyAo1gjCJwTOdmSeFjphBOgH_OYU-j9awBM,AIzaSyCcgSeznPu_I75xhxOk-dr7DdIG5unaeQM")

# 假流式是否开启
FAKE_STREAMING = os.environ.get("FAKE_STREAMING", "true").lower() in ["true", "1", "yes"]

# 配置持久化存储目录
STORAGE_DIR = os.environ.get("STORAGE_DIR", "/hajimi/settings/")
ENABLE_STORAGE = os.environ.get("ENABLE_STORAGE", "false").lower() in ["true", "1", "yes"]

# 并发请求配置
CONCURRENT_REQUESTS = int(os.environ.get("CONCURRENT_REQUESTS", "5"))  # 默认并发请求数
INCREASE_CONCURRENT_ON_FAILURE = int(os.environ.get("INCREASE_CONCURRENT_ON_FAILURE", "0"))  # 失败时增加的并发数
MAX_CONCURRENT_REQUESTS = int(os.environ.get("MAX_CONCURRENT_REQUESTS", "1"))  # 最大并发请求数

# 缓存配置
CACHE_EXPIRY_TIME = int(os.environ.get("CACHE_EXPIRY_TIME", "21600"))  # 默认缓存 6 小时 (21600 秒)
MAX_CACHE_ENTRIES = int(os.environ.get("MAX_CACHE_ENTRIES", "500"))  # 默认最多缓存500条响应
CALCULATE_CACHE_ENTRIES = int(os.environ.get("CALCULATE_CACHE_ENTRIES", "6"))  # 默认取最后 6 条消息算缓存键
PRECISE_CACHE = os.environ.get("PRECISE_CACHE", "false").lower() in ["true", "1", "yes"] #是否取所有消息来算缓存键

# 是否启用 Vertex AI
ENABLE_VERTEX = os.environ.get("ENABLE_VERTEX", "false").lower() in ["true", "1", "yes"]
GOOGLE_CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON", "")

# 是否启用快速模式 Vertex
ENABLE_VERTEX_EXPRESS = os.environ.get("ENABLE_VERTEX_EXPRESS", "false").lower() in ["true", "1", "yes"]
VERTEX_EXPRESS_API_KEY = os.environ.get("VERTEX_EXPRESS_API_KEY", "")

# 联网搜索配置
search={
    "search_mode":os.environ.get("SEARCH_MODE", "false").lower() in ["false", "0", "no"],
    "search_prompt":os.environ.get("SEARCH_PROMPT", "（使用搜索工具联网搜索，需要在content中结合搜索内容）").strip('"')
}

#随机字符串
RANDOM_STRING = os.environ.get("RANDOM_STRING", "true").lower() in ["true", "1", "yes"]
RANDOM_STRING_LENGTH = int(os.environ.get("RANDOM_STRING_LENGTH", "0"))

# 空响应重试次数限制
MAX_EMPTY_RESPONSES = int(os.environ.get("MAX_EMPTY_RESPONSES", "3"))  # 默认最多允许3次空响应

# ---------- 以下是其他配置信息 ----------

# 访问限制
MAX_RETRY_NUM = int(os.environ.get("MAX_RETRY_NUM", "5")) # 请求时的最大总轮询 key 数
MAX_REQUESTS_PER_MINUTE = int(os.environ.get("MAX_REQUESTS_PER_MINUTE", "300")) 
MAX_REQUESTS_PER_DAY_PER_IP = int(os.environ.get("MAX_REQUESTS_PER_DAY_PER_IP", "6000000"))

# API密钥使用限制
API_KEY_DAILY_LIMIT = int(os.environ.get("API_KEY_DAILY_LIMIT", "100"))# 默认每个API密钥每24小时可使用100次

# 模型屏蔽黑名单，格式应为逗号分隔的模型名称集合
BLOCKED_MODELS = { model.strip() for model in os.environ.get("BLOCKED_MODELS", "").split(",") if model.strip() }

#公益站模式
PUBLIC_MODE = os.environ.get("PUBLIC_MODE", "false").lower() in ["true", "1", "yes"]
#前端地址
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "")

# 模型屏蔽白名单
WHITELIST_MODELS = { x.strip() for x in os.environ.get("WHITELIST_MODELS", "").split(",") if x.strip() }
# 白名单User-Agent
WHITELIST_USER_AGENT = { x.strip().lower() for x in os.environ.get("WHITELIST_USER_AGENT", "").split(",") if x.strip() }

# 跨域配置
# 允许的源列表，逗号分隔，例如 "http://localhost:3000,https://example.com"
ALLOWED_ORIGINS_STR = os.environ.get("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_STR.split(",") if origin.strip()]

# ---------- 运行时全局信息，无需修改 ----------

# 基础目录设置
BASE_DIR = pathlib.Path(__file__).parent.parent

# 失效的API密钥
INVALID_API_KEYS = os.environ.get("INVALID_API_KEYS", "")

version={
    "local_version":"0.0.0",
    "remote_version":"0.0.0",
    "has_update":False
}

# API调用统计
# 这个对象保留为空结构以保持向后兼容性
# 实际统计数据已迁移到 app/utils/stats.py 中的 ApiStatsManager 类
api_call_stats = {
    'calls': []  # 兼容旧版代码结构
}

# 用于保护 api_call_stats 并发访问的锁
stats_lock = asyncio.Lock() 

# 日志配置
logging.getLogger("uvicorn").disabled = True
logging.getLogger("uvicorn.access").disabled = True


# ---------- 以下配置信息已废弃 ----------

# 假流式请求的空内容返回间隔（秒）
FAKE_STREAMING_INTERVAL = float(os.environ.get("FAKE_STREAMING_INTERVAL", "1"))
# 假流式响应的每个块大小
FAKE_STREAMING_CHUNK_SIZE = int(os.environ.get("FAKE_STREAMING_CHUNK_SIZE", "10"))
# 假流式响应的每个块之间的延迟（秒）
FAKE_STREAMING_DELAY_PER_CHUNK = float(os.environ.get("FAKE_STREAMING_DELAY_PER_CHUNK", "0.1"))

# 非流式请求TCP保活配置
NONSTREAM_KEEPALIVE_ENABLED = os.environ.get("NONSTREAM_KEEPALIVE_ENABLED", "true").lower() in ["true", "1", "yes"]
NONSTREAM_KEEPALIVE_INTERVAL = float(os.environ.get("NONSTREAM_KEEPALIVE_INTERVAL", "5.0"))
