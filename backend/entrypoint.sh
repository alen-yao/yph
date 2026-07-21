#!/bin/bash
set -e

echo "等待数据库连接..."
while ! nc -z ${DATABASE_HOST:-mysql} ${DATABASE_PORT:-3306}; do
  sleep 1
done
echo "数据库已连接！"

echo "执行数据库迁移..."
python manage.py migrate --noinput

echo "收集静态文件..."
python manage.py collectstatic --noinput

echo "启动 Django 服务器..."
if [ "${DEBUG}" = "True" ]; then
  echo "开发模式 - 使用 runserver"
  python manage.py runserver 0.0.0.0:8000
else
  echo "生产模式 - 使用 gunicorn"
  gunicorn yph.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2 --timeout 60 --access-logfile - --error-logfile -
fi
