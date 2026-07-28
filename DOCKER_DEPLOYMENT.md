# 🐳 Docker Compose 一键部署指南

## 📋 服务架构

本项目使用 Docker Compose 编排以下服务：

| 服务 | 镜像 | 端口 | 说明 |
|------|------|------|------|
| **mysql** | mysql:8.0 | 3306 | MySQL 数据库 |
| **redis** | redis:7-alpine | 6379 | Redis 缓存 |
| **minio** | minio/minio:latest | 9000, 9001 | MinIO 对象存储 |
| **backend** | 自定义构建 | 8000 | Django 后端 API |
| **celery-worker** | 自定义构建 | - | Celery 异步任务 |
| **admin** | 自定义构建 | 3000 | 管理后台前端 |
| **h5** | 自定义构建 | 3001 | H5 移动端前端 |
| **pc** | 自定义构建 | 8080 | PC 端前端 |
| **nginx** | nginx:alpine | 80, 443 | 反向代理 |

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

### 2. 配置环境变量（可选）

如果使用默认配置，可以跳过此步骤。如需自定义配置：

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（生产环境必须修改密码）
vim .env
```

**生产环境必须修改的配置：**
```bash
# 数据库密码
MYSQL_ROOT_PASSWORD=your-secure-password
MYSQL_PASSWORD=your-secure-password

# Redis 密码
REDIS_PASSWORD=your-secure-password

# Django 密钥
SECRET_KEY=your-long-random-secret-key

# MinIO 访问密钥
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key

# 域名配置
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
MINIO_PUBLIC_URL=http://yourdomain.com:9000
```

### 3. 启动所有服务

```bash
# 启动所有服务（后台运行）
docker-compose up -d

# 查看启动日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f minio
```

### 4. 初始化数据库

```bash
# 等待 MySQL 启动完成（约 30 秒）
docker-compose exec backend python manage.py migrate

# 创建超级管理员
docker-compose exec backend python manage.py createsuperuser

# 收集静态文件
docker-compose exec backend python manage.py collectstatic --noinput
```

### 5. 访问服务

| 服务 | 地址 | 说明 |
|------|------|------|
| **管理后台** | http://localhost:3000 | 管理员界面 |
| **H5 端** | http://localhost:3001 | 移动端界面 |
| **PC 端** | http://localhost:8080 | PC 端界面 |
| **后端 API** | http://localhost:8000 | Django REST API |
| **API 文档** | http://localhost:8000/swagger/ | Swagger 文档 |
| **MinIO 控制台** | http://localhost:9001 | MinIO 管理界面 |
| **Nginx** | http://localhost:80 | 反向代理 |

### 6. MinIO 初始化

首次启动后，访问 MinIO 控制台初始化：

1. 访问 http://localhost:9001
2. 使用配置的账号密码登录（默认: minioadmin/minioadmin）
3. MinIO 客户端会自动创建 `yph-products` 存储桶
4. 测试上传功能

```bash
# 测试 MinIO 连接
docker-compose exec backend python test_minio.py
```

## 📦 常用命令

### 服务管理

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启特定服务
docker-compose restart backend
docker-compose restart minio

# 查看服务状态
docker-compose ps

# 查看资源使用
docker stats
```

### 日志查看

```bash
# 查看所有日志
docker-compose logs

# 实时查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f minio

# 查看最近 100 行日志
docker-compose logs --tail=100 backend
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入 MySQL 容器
docker-compose exec mysql mysql -u root -p

# 进入 Redis 容器
docker-compose exec redis redis-cli -a redis123456

# 进入 MinIO 容器
docker-compose exec minio sh
```

### 数据库管理

```bash
# 运行数据库迁移
docker-compose exec backend python manage.py migrate

# 创建迁移文件
docker-compose exec backend python manage.py makemigrations

# 执行 Django 命令
docker-compose exec backend python manage.py shell

# 备份数据库
docker-compose exec mysql mysqldump -u root -pyph2024! yph > backup.sql

# 恢复数据库
docker-compose exec -T mysql mysql -u root -pyph2024! yph < backup.sql
```

### MinIO 管理

```bash
# 查看 MinIO 数据
docker-compose exec minio ls /data

# 重启 MinIO
docker-compose restart minio

# 查看 MinIO 日志
docker-compose logs -f minio

# 备份 MinIO 数据
docker cp yph-minio:/data ./minio_backup
```

## 🔧 服务配置详解

### MinIO 配置

MinIO 服务配置在 `docker-compose.yml`:

```yaml
minio:
  image: minio/minio:latest
  container_name: yph-minio
  restart: always
  environment:
    MINIO_ROOT_USER: ${MINIO_ACCESS_KEY:-minioadmin}
    MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY:-minioadmin}
  command: server /data --console-address ":9001"
  ports:
    - "9000:9000"   # API 端口
    - "9001:9001"   # 控制台端口
  volumes:
    - minio_data:/data
```

**重要配置项：**
- `MINIO_ROOT_USER`: MinIO 访问密钥
- `MINIO_ROOT_PASSWORD`: MinIO 密钥
- 数据持久化在 `minio_data` 卷中
- API 端口: 9000（供应用程序访问）
- 控制台端口: 9001（供管理员访问）

### 后端 MinIO 环境变量

```yaml
backend:
  environment:
    - MINIO_ENDPOINT=minio:9000           # 容器内访问地址
    - MINIO_ACCESS_KEY=minioadmin
    - MINIO_SECRET_KEY=minioadmin
    - MINIO_BUCKET_NAME=yph-products
    - MINIO_SECURE=False                  # 容器内不使用 HTTPS
    - MINIO_PUBLIC_URL=http://localhost:9000  # 外部访问地址
```

**注意事项：**
- `MINIO_ENDPOINT` 使用容器名 `minio`（容器间通信）
- `MINIO_PUBLIC_URL` 使用外部地址（返回给前端的 URL）

## 🌐 网络配置

所有服务都在同一个桥接网络 `yph-network` 中：

```yaml
networks:
  yph-network:
    driver: bridge
```

**服务间通信：**
- 后端访问 MySQL: `mysql:3306`
- 后端访问 Redis: `redis:6379`
- 后端访问 MinIO: `minio:9000`
- 前端访问后端: 通过 `VITE_API_BASE_URL` 配置

## 💾 数据持久化

所有数据都持久化到 Docker 卷中：

```yaml
volumes:
  mysql_data:      # MySQL 数据
  redis_data:      # Redis 数据
  minio_data:      # MinIO 对象存储数据
```

### 数据备份

```bash
# 备份所有数据卷
docker run --rm -v yph_mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_backup.tar.gz -C /data .
docker run --rm -v yph_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_backup.tar.gz -C /data .
docker run --rm -v yph_minio_data:/data -v $(pwd):/backup alpine tar czf /backup/minio_backup.tar.gz -C /data .
```

### 数据恢复

```bash
# 恢复数据卷
docker run --rm -v yph_mysql_data:/data -v $(pwd):/backup alpine tar xzf /backup/mysql_backup.tar.gz -C /data
docker run --rm -v yph_redis_data:/data -v $(pwd):/backup alpine tar xzf /backup/redis_backup.tar.gz -C /data
docker run --rm -v yph_minio_data:/data -v $(pwd):/backup alpine tar xzf /backup/minio_backup.tar.gz -C /data
```

## 🔍 健康检查

所有服务都配置了健康检查：

```bash
# 查看服务健康状态
docker-compose ps

# 健康的服务会显示 "healthy"
# 不健康的服务会显示 "unhealthy"
```

**健康检查配置：**
- MySQL: `mysqladmin ping`
- Backend: `curl http://localhost:8000/api/health/`
- MinIO: `curl http://localhost:9000/minio/health/live`
- Nginx: `wget http://localhost:80/health`

## 🚨 故障排查

### MinIO 无法启动

```bash
# 查看 MinIO 日志
docker-compose logs minio

# 检查端口占用
netstat -tuln | grep 9000
netstat -tuln | grep 9001

# 重新创建 MinIO 容器
docker-compose rm -f minio
docker-compose up -d minio
```

### 后端无法连接 MinIO

```bash
# 检查网络连通性
docker-compose exec backend ping minio

# 检查 MinIO 是否健康
docker-compose ps minio

# 查看后端环境变量
docker-compose exec backend env | grep MINIO

# 测试 MinIO 连接
docker-compose exec backend python test_minio.py
```

### 图片上传失败

```bash
# 检查 MinIO 存储桶
docker-compose exec backend python manage.py shell
>>> from utils.minio_client import minio_client
>>> minio_client.client.bucket_exists('yph-products')

# 查看后端日志
docker-compose logs -f backend | grep -i minio
```

### 服务无法访问

```bash
# 检查所有服务状态
docker-compose ps

# 检查网络配置
docker network inspect yph_yph-network

# 重启所有服务
docker-compose restart
```

## 📈 性能优化

### 生产环境建议

1. **调整资源限制**

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

2. **启用日志轮转**

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

3. **调整 MinIO 内存**

MinIO 默认会使用大量内存，可以限制：

```yaml
minio:
  environment:
    MINIO_CACHE_SIZE: "2GB"
```

4. **使用 CDN**

生产环境建议在 MinIO 前配置 CDN 加速图片访问。

## 🔐 安全建议

### 生产环境必做

1. **修改所有默认密码**
   - MySQL root 密码
   - Redis 密码
   - MinIO 访问密钥
   - Django SECRET_KEY

2. **启用 HTTPS**
   - 配置 SSL 证书
   - 修改 `MINIO_SECURE=True`
   - 使用 Let's Encrypt

3. **限制端口暴露**
   - 只暴露 Nginx 80/443 端口
   - 其他服务端口仅在内网访问

4. **配置防火墙**
   ```bash
   # 只允许 80 和 443 端口
   ufw allow 80
   ufw allow 443
   ufw enable
   ```

5. **定期备份**
   - 设置定时任务备份数据库
   - 备份 MinIO 数据
   - 备份到远程存储

## 📚 参考文档

- [Docker Compose 文档](https://docs.docker.com/compose/)
- [MinIO 文档](https://min.io/docs/)
- [Django 部署](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Nginx 配置](https://nginx.org/en/docs/)

---

**部署日期**: 2026-07-27  
**版本**: v1.0
