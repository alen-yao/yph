# ✅ MinIO 已集成到 Docker Compose

## 🎉 完成内容

MinIO 对象存储已完全集成到 Docker Compose 部署方案中，实现一键启动所有服务。

## 📝 核心变更

### 1. docker-compose.yml 新增 MinIO 服务

```yaml
# MinIO 对象存储
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
  networks:
    - yph-network
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
    interval: 30s
    timeout: 10s
    retries: 3
```

### 2. 后端服务自动连接 MinIO

```yaml
backend:
  environment:
    # MinIO 连接配置
    - MINIO_ENDPOINT=minio:9000              # 容器内访问
    - MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
    - MINIO_SECRET_KEY=${MINIO_SECRET_KEY}
    - MINIO_BUCKET_NAME=${MINIO_BUCKET_NAME:-yph-products}
    - MINIO_SECURE=False
    - MINIO_PUBLIC_URL=${MINIO_PUBLIC_URL:-http://localhost:9000}
  depends_on:
    - minio  # 等待 MinIO 启动
```

### 3. 数据持久化

```yaml
volumes:
  minio_data:  # MinIO 数据持久化卷
    driver: local
```

### 4. 环境变量配置

新增到 `.env.example`:

```bash
# MinIO 对象存储配置
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=yph-products
MINIO_API_PORT=9000
MINIO_CONSOLE_PORT=9001
MINIO_PUBLIC_URL=http://localhost:9000
```

## 🚀 使用方法

```bash
# 1. 配置环境变量（可选，使用默认配置可跳过）
cp .env.example .env

# 2. 启动所有服务
docker-compose up -d

# 3. 初始化数据库
docker-compose exec backend python manage.py migrate

# 4. 测试 MinIO 连接
docker-compose exec backend python test_minio.py

# 5. 查看服务状态
docker-compose ps
```

## 🌐 服务访问

启动后可访问：

| 服务 | 地址 | 账号 |
|------|------|------|
| MinIO 控制台 | http://localhost:9001 | minioadmin / minioadmin |
| MinIO API | http://localhost:9000 | - |
| 后端 API | http://localhost:8000 | - |
| 管理后台 | http://localhost:3000 | - |

## 🔧 服务间通信

Docker Compose 自动配置服务间通信：

```
backend 容器
   ↓ (访问 minio:9000)
minio 容器
```

**重要说明:**
- 容器内访问: `MINIO_ENDPOINT=minio:9000` (使用容器名)
- 外部访问: `MINIO_PUBLIC_URL=http://localhost:9000` (使用主机地址)
- 前端通过 URL 访问图片: 后端返回 `MINIO_PUBLIC_URL` 的完整 URL

## 📦 数据持久化

MinIO 数据存储在 Docker 卷中，即使删除容器也不会丢失：

```bash
# 查看数据卷
docker volume ls | grep minio

# 备份 MinIO 数据
docker run --rm -v yph_minio_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/minio_backup.tar.gz -C /data .

# 恢复 MinIO 数据
docker run --rm -v yph_minio_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/minio_backup.tar.gz -C /data
```

## 🔍 健康检查

MinIO 配置了健康检查，确保服务正常运行：

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
  interval: 30s
  timeout: 10s
  retries: 3
```

查看健康状态：

```bash
docker-compose ps
# MinIO 显示 "healthy" 表示正常
```

## 🛠️ 常用操作

### 查看 MinIO 日志

```bash
docker-compose logs -f minio
```

### 重启 MinIO

```bash
docker-compose restart minio
```

### 进入 MinIO 容器

```bash
docker-compose exec minio sh
```

### 查看存储桶

```bash
docker-compose exec backend python manage.py shell
>>> from utils.minio_client import minio_client
>>> minio_client.client.list_buckets()
```

## 🎯 完整工作流程

### 1. 启动项目

```bash
./start.sh
```

### 2. 访问 MinIO 控制台

浏览器打开 http://localhost:9001，使用 `minioadmin/minioadmin` 登录

### 3. 上传产品图片

```bash
# 方式A: 通过 API 上传
curl -X POST http://localhost:8000/api/system/upload/image/ \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@product.jpg"

# 返回: {"url": "http://localhost:9000/yph-products/products/abc123.jpg"}
```

### 4. 创建商品

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "商品名称",
    "price": 99.00,
    "main_images": ["http://localhost:9000/yph-products/products/abc123.jpg"],
    "detail_images": []
  }'
```

### 5. 前端展示

前端直接使用返回的 URL 显示图片，无需特殊处理。

## 🔐 生产环境配置

### 1. 修改 MinIO 密钥

```bash
# .env 文件
MINIO_ACCESS_KEY=your-secure-access-key
MINIO_SECRET_KEY=your-secure-secret-key-min-8-chars
```

### 2. 使用 HTTPS

```bash
# .env 文件
MINIO_PUBLIC_URL=https://cdn.yourdomain.com
MINIO_SECURE=True
```

### 3. 配置 Nginx 反向代理

```nginx
# nginx/conf.d/minio.conf
server {
    listen 80;
    server_name cdn.yourdomain.com;

    location / {
        proxy_pass http://minio:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 文件大小限制
        client_max_body_size 100M;
    }
}
```

### 4. 配置 SSL 证书

```bash
# 使用 Let's Encrypt
certbot --nginx -d cdn.yourdomain.com
```

## 📊 网络架构

```
外部访问
   ↓
http://localhost:9001 (MinIO 控制台)
http://localhost:9000 (MinIO API)
   ↓
yph-network (Docker 桥接网络)
   ↓
┌─────────────┐     ┌──────────────┐
│   Backend   │ ←→  │    MinIO     │
│  (Django)   │     │  (minio:9000)│
└─────────────┘     └──────────────┘
   ↓ 存储图片URL            ↓ 存储文件
┌─────────────┐     ┌──────────────┐
│    MySQL    │     │ minio_data 卷│
└─────────────┘     └──────────────┘
```

## ✅ 优势

1. **一键部署**: 所有服务统一管理，一个命令启动
2. **自动配置**: 网络、依赖关系自动处理
3. **数据持久化**: 数据卷自动管理，不会丢失
4. **健康检查**: 自动监控服务状态
5. **容器间通信**: 无需配置 IP，使用服务名访问
6. **环境隔离**: 开发、测试、生产环境独立

## 📚 相关文档

- [QUICK_START.md](QUICK_START.md) - 快速开始指南
- [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) - Docker 部署详解
- [backend/README_MINIO.md](backend/README_MINIO.md) - MinIO 使用指南
- [backend/docs/PRODUCT_IMAGES.md](backend/docs/PRODUCT_IMAGES.md) - 产品图片管理

---

**集成日期**: 2026-07-27  
**版本**: v1.0  
**状态**: ✅ 已完成并测试
