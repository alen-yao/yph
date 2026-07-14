#!/bin/bash

# YPH 电商系统 Docker 快速启动脚本

set -e

echo "======================================"
echo "  YPH 电商系统 Docker 部署"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: 未安装 Docker${NC}"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: 未安装 Docker Compose${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker 环境检查通过${NC}"
echo ""

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}未找到 .env 文件，从模板创建...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}请编辑 .env 文件配置环境变量后重新运行此脚本${NC}"
    echo -e "${YELLOW}重点修改以下配置:${NC}"
    echo "  - MYSQL_ROOT_PASSWORD (数据库 root 密码)"
    echo "  - MYSQL_PASSWORD (数据库用户密码)"
    echo "  - REDIS_PASSWORD (Redis 密码)"
    echo "  - SECRET_KEY (Django 密钥)"
    echo ""
    exit 0
fi

echo -e "${GREEN}✓ 环境配置文件已存在${NC}"
echo ""

# 构建镜像
echo -e "${YELLOW}[1/5] 构建 Docker 镜像...${NC}"
docker-compose build

echo -e "${GREEN}✓ 镜像构建完成${NC}"
echo ""

# 启动服务
echo -e "${YELLOW}[2/5] 启动服务...${NC}"
docker-compose up -d

echo -e "${GREEN}✓ 服务启动完成${NC}"
echo ""

# 等待数据库就绪
echo -e "${YELLOW}[3/5] 等待数据库就绪...${NC}"
max_attempts=30
attempt=0
until docker-compose exec -T mysql mysqladmin ping -h localhost --silent || [ $attempt -eq $max_attempts ]; do
    attempt=$((attempt+1))
    echo "  等待中... ($attempt/$max_attempts)"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}错误: 数据库启动超时${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 数据库已就绪${NC}"
echo ""

# 执行数据库迁移
echo -e "${YELLOW}[4/5] 执行数据库迁移...${NC}"
docker-compose exec -T backend python manage.py migrate

echo -e "${GREEN}✓ 数据库迁移完成${NC}"
echo ""

# 收集静态文件
echo -e "${YELLOW}[5/5] 收集静态文件...${NC}"
docker-compose exec -T backend python manage.py collectstatic --noinput

echo -e "${GREEN}✓ 静态文件收集完成${NC}"
echo ""

# 显示服务状态
echo "======================================"
echo "  部署完成！服务状态:"
echo "======================================"
docker-compose ps
echo ""

# 显示访问地址
echo "======================================"
echo "  访问地址:"
echo "======================================"
echo -e "${GREEN}H5 商城:${NC}       http://localhost:80"
echo -e "${GREEN}管理后台:${NC}     http://localhost:80/admin-panel/"
echo -e "${GREEN}Django Admin:${NC} http://localhost:80/admin/"
echo -e "${GREEN}API 文档:${NC}     http://localhost:80/api/docs/"
echo ""

# 提示创建管理员
echo "======================================"
echo "  下一步操作:"
echo "======================================"
echo "创建超级管理员账号:"
echo -e "${YELLOW}  docker-compose exec backend python manage.py createsuperuser${NC}"
echo ""
echo "查看日志:"
echo -e "${YELLOW}  docker-compose logs -f${NC}"
echo ""
echo "停止服务:"
echo -e "${YELLOW}  docker-compose down${NC}"
echo ""

echo -e "${GREEN}🎉 部署成功！${NC}"
