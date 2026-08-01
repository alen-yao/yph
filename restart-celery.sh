#!/bin/bash
# 重新构建并启动 celery-worker

echo "停止并删除旧的 celery-worker 容器..."
docker-compose stop celery-worker
docker-compose rm -f celery-worker

echo "重新构建 backend 镜像..."
docker-compose build backend celery-worker

echo "启动 celery-worker..."
docker-compose up -d celery-worker

echo "查看 celery-worker 日志..."
docker-compose logs -f celery-worker
