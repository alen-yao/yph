# Gunicorn 配置文件
import multiprocessing
import os

# 服务器套接字
bind = "0.0.0.0:8000"
backlog = 2048

# Worker 进程
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 60
keepalive = 2

# 线程
threads = int(os.getenv("GUNICORN_THREADS", 2))

# 日志
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程命名
proc_name = "yph-backend"

# 服务器机制
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# 重载
reload = os.getenv("DEBUG", "False") == "True"
reload_engine = "auto"

# SSL (生产环境由 Nginx 处理)
# keyfile = None
# certfile = None
