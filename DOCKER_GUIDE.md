# YPH 电商系统 Docker 部署指南

## 📦 项目架构

```
┌─────────────────────────────────────────┐
│          Nginx (反向代理)                │
│     - 路由分发                           │
│     - 静态文件服务                        │
│     - 负载均衡                           │
└──────────┬──────────────────────────────┘
           │
    ┌──────┴───────┬──────────┬──────────┐
    │              │          │          │
┌───▼────┐  ┌─────▼──┐  ┌────▼───┐  ┌──▼─────┐
│Backend │  │ Admin  │  │  H5    │  │ MySQL  │
│Django  │  │ Vue3   │  │ Vue3   │  │ Redis  │
└────────┘  └────────┘  └────────┘  └────────┘
```

## 🚀 快速开始

### 1. 环境准备

确保已安装：
- Docker (>= 20.10)
- Docker Compose (>= 2.0)

```bash
# 检查版本
docker --version
docker-compose --version
```

### 2. 初始化配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量（重要！）
# 修改数据库密码、Django SECRET_KEY 等
nano .env
```

### 3. 首次部署

```bash
# 方法 1: 使用 Makefile（推荐）
make init          # 初始化配置
make first-deploy  # 首次部署

# 方法 2: 手动执行
docker-compose build
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose exec backend python manage.py createsuperuser
```

### 4. 访问服务

- **H5 商城**: http://localhost:80
- **管理后台**: http://localhost:80/admin-panel/
- **Django Admin**: http://localhost:80/admin/
- **API 文档**: http://localhost:80/swagger/

## 🛠️ 常用命令

### 服务管理

```bash
# 启动服务
make up
# 或
docker-compose up -d

# 停止服务
make down
# 或
docker-compose down

# 重启服务
make restart
# 或
docker-compose restart

# 查看服务状态
make ps
# 或
docker-compose ps

# 查看日志
make logs
# 或
docker-compose logs -f [服务名]
```

### 数据库操作

```bash
# 执行迁移
make migrate
# 或
docker-compose exec backend python manage.py migrate

# 创建超级管理员
make createsuperuser
# 或
docker-compose exec backend python manage.py createsuperuser

# 进入 MySQL
docker-compose exec mysql mysql -u yph -p
```

### 开发调试

```bash
# 进入后端容器
make shell
# 或
docker-compose exec backend /bin/bash

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f nginx

# 重新构建镜像
docker-compose build --no-cache backend
```

## 🔧 优化特性

### 1. 多阶段构建
- **后端**: Python 依赖分离，减少镜像大小
- **前端**: 构建和运行阶段分离，最终镜像仅 ~20MB

### 2. 缓存优化
- 依赖文件单独 COPY，利用 Docker 层缓存
- 前端使用 `npm ci` 提升安装速度
- Nginx 配置静态资源缓存策略

### 3. 性能优化
- Nginx 反向代理和负载均衡
- Gzip 压缩减少传输大小
- MySQL 连接池和缓冲优化
- Redis 持久化配置

### 4. 安全增强
- 非 root 用户运行应用
- 环境变量管理敏感信息
- 健康检查确保服务可用
- 安全头防护 XSS/点击劫持

### 5. 生产就绪
- Gunicorn 作为 WSGI 服务器
- Celery 异步任务支持
- 数据卷持久化
- 自动重启策略

## 📊 资源监控

### 查看资源使用

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
docker system df

# 清理未使用资源
docker system prune -a
```

## 🔒 生产环境配置

### 1. 环境变量

在 `.env` 中设置：

```bash
# 安全配置
DEBUG=False
SECRET_KEY=your-very-long-and-random-secret-key

# 允许的域名
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# 数据库密码（强密码）
MYSQL_ROOT_PASSWORD=VeryStrongPassword123!
MYSQL_PASSWORD=StrongDBPassword456!
REDIS_PASSWORD=StrongRedisPassword789!
```

### 2. HTTPS 配置

1. 将 SSL 证书放到 `nginx/ssl/` 目录
2. 编辑 `nginx/conf.d/yph.conf`，取消 HTTPS server 注释
3. 重启 nginx: `docker-compose restart nginx`

### 3. 备份策略

```bash
# 备份数据库
docker-compose exec mysql mysqldump -u yph -p yph > backup_$(date +%Y%m%d).sql

# 备份 Redis
docker-compose exec redis redis-cli --rdb /data/backup.rdb

# 备份媒体文件
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/
```

## 🐛 故障排查

### 常见问题

#### 1. 服务无法启动

```bash
# 查看详细日志
docker-compose logs [服务名]

# 检查端口占用
netstat -tuln | grep [端口号]
```

#### 2. 数据库连接失败

```bash
# 检查 MySQL 健康状态
docker-compose ps mysql

# 查看 MySQL 日志
docker-compose logs mysql

# 手动测试连接
docker-compose exec backend python manage.py dbshell
```

#### 3. 前端无法访问后端

- 检查 `VITE_API_BASE_URL` 环境变量
- 确认 Nginx 反向代理配置
- 查看浏览器控制台 CORS 错误

#### 4. 静态文件 404

```bash
# 重新收集静态文件
docker-compose exec backend python manage.py collectstatic --noinput

# 检查 Nginx 挂载
docker-compose exec nginx ls -la /usr/share/nginx/html/static/
```

## 📝 开发模式

开发时可以使用 volume 挂载实现热重载：

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  backend:
    volumes:
      - ./backend:/app
    environment:
      - DEBUG=True
    command: python manage.py runserver 0.0.0.0:8000
  
  admin:
    volumes:
      - ./frontend/admin:/app
    command: npm run dev
```

## 🎯 性能调优

### 1. Gunicorn 配置

根据服务器配置调整 workers 数量：
```
workers = (2 * CPU核心数) + 1
```

### 2. MySQL 优化

在 `docker-compose.yml` 中调整：
```yaml
command:
  - --innodb_buffer_pool_size=2G  # 根据内存调整
  - --max_connections=500
```

### 3. Nginx 优化

```nginx
worker_processes auto;  # 自动根据 CPU 核心数
worker_connections 4096;  # 增加连接数
```

## 📚 更多资源

- [Django 官方文档](https://docs.djangoproject.com/)
- [Vue3 官方文档](https://vuejs.org/)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)
- [Nginx 配置指南](https://nginx.org/en/docs/)

## 🆘 获取帮助

```bash
# 查看 Makefile 所有命令
make help

# 导出配置供调试
docker-compose config > debug-config.yml
```

---

**Made with ❤️ by YPH Team**
