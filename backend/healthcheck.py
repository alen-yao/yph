"""
健康检查端点
在 urls.py 中添加这个视图
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """
    健康检查端点
    检查数据库和 Redis 连接
    """
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "cache": "unknown"
    }

    status_code = 200

    # 检查数据库连接
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        status_code = 503

    # 检查 Redis 缓存
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            health_status["cache"] = "connected"
        else:
            raise Exception("Cache write/read failed")
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        health_status["cache"] = "disconnected"
        health_status["status"] = "unhealthy"
        status_code = 503

    return JsonResponse(health_status, status=status_code)
