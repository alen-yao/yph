.PHONY: help build up down restart logs clean ps migrate collectstatic createsuperuser

help:
	@echo "YPH 电商系统 Docker 命令"
	@echo ""
	@echo "使用方法: make [命令]"
	@echo ""
	@echo "命令列表:"
	@echo "  build           - 构建所有 Docker 镜像"
	@echo "  up              - 启动所有服务"
	@echo "  down            - 停止所有服务"
	@echo "  restart         - 重启所有服务"
	@echo "  logs            - 查看所有服务日志"
	@echo "  ps              - 查看运行中的容器"
	@echo "  clean           - 清理所有容器、镜像和数据卷"
	@echo "  migrate         - 执行数据库迁移"
	@echo "  collectstatic   - 收集静态文件"
	@echo "  createsuperuser - 创建超级管理员"
	@echo "  shell           - 进入后端容器 shell"
	@echo "  test            - 运行测试"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

ps:
	docker-compose ps

clean:
	docker-compose down -v --rmi all --remove-orphans

migrate:
	docker-compose exec backend python manage.py migrate

collectstatic:
	docker-compose exec backend python manage.py collectstatic --noinput

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

shell:
	docker-compose exec backend /bin/bash

test:
	docker-compose exec backend python manage.py test

# 快速启动（首次部署）
init:
	@echo "初始化 YPH 电商系统..."
	cp .env.example .env
	@echo "请编辑 .env 文件设置环境变量"
	@echo "然后运行: make first-deploy"

first-deploy: build up
	@echo "等待服务启动..."
	sleep 10
	make migrate
	make collectstatic
	@echo "部署完成！请运行 'make createsuperuser' 创建管理员账号"
