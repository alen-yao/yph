#!/bin/bash
# YPH 电商系统快速启动脚本

echo "======================================"
echo "YPH 电商系统启动脚本"
echo "======================================"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 创建超级用户（如果不存在）
echo "如果需要创建超级用户，请执行: python manage.py createsuperuser"

# 启动服务
echo "======================================"
echo "启动开发服务器..."
echo "API 文档: http://localhost:8000/api/docs/"
echo "管理后台: http://localhost:8000/admin/"
echo "======================================"
python manage.py runserver 0.0.0.0:8000
