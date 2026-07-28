# 🚀 YPH 电商系统 - 快速开始指南

## 📋 一分钟了解项目

**YPH 电商系统** 是一个完整的全栈电商解决方案，包含：

- ✅ **后端**: Django + DRF + MySQL + Redis + MinIO
- ✅ **前端**: Vue 3 管理后台 + H5 移动端 + PC 商城
- ✅ **对象存储**: MinIO 用于图片、文件管理
- ✅ **容器化**: Docker Compose 一键部署
- ✅ **功能完善**: 商品管理、订单系统、支付集成、营销活动

## ⚡ 快速启动

```bash
# 1. 克隆项目
git clone <repository-url>
cd yph

# 2. 配置环境变量（可选，使用默认配置）
cp .env.example .env

# 3. 启动所有服务
docker-compose up -d

# 4. 初始化数据库
docker-compose exec backend python manage.py migrate

# 5. 创建管理员账号（可选）
docker-compose exec backend python manage.py createsuperuser

# 6. 测试 MinIO 连接
docker-compose exec backend python test_minio.py
```

**就这么简单！** 所有服务会自动启动并完成配置。

## 🌐 访问服务

启动完成后，访问以下地址：

| 服务 | 地址 | 说明 |
|------|------|------|
| 🖥️ **管理后台** | http://localhost:3000 | 商家管理界面 |
| 📱 **H5 移动端** | http://localhost:3001 | 用户购物界面 |
| 💻 **PC 商城** | http://localhost:8080 | PC 端商城 |
| 🔧 **后端 API** | http://localhost:8000 | RESTful API |
| 📖 **API 文档** | http://localhost:8000/swagger/ | Swagger 文档 |
| 📦 **MinIO 控制台** | http://localhost:9001 | 对象存储管理 |

### MinIO 默认账号

```
用户名: minioadmin
密码: minioadmin
```

## 🛠️ 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f minio

# 停止服务（保留数据）
docker-compose down

# 停止服务并删除数据卷（删除所有数据）
docker-compose down -v

# 重启服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
docker-compose restart minio

# 进入后端容器
docker-compose exec backend bash

# 创建管理员账号
docker-compose exec backend python manage.py createsuperuser
```

## 📂 项目结构

```
yph/
├── backend/              # Django 后端
│   ├── apps/            # 应用模块
│   │   ├── products/    # 商品管理（✅ 已集成 MinIO 多图）
│   │   ├── users/       # 用户管理
│   │   ├── trade/       # 交易订单
│   │   ├── marketing/   # 营销活动
│   │   ├── payment/     # 支付系统
│   │   └── system/      # 系统配置（✅ 图片上传 API）
│   ├── utils/           # 工具类
│   │   └── minio_client.py  # ✅ MinIO 客户端
│   └── docs/            # 后端文档
│       ├── MINIO_INTEGRATION.md    # MinIO 集成指南
│       └── PRODUCT_IMAGES.md       # 产品图片管理
├── frontend/
│   ├── admin/           # Vue 3 管理后台
│   ├── h5/              # H5 移动端
│   └── pc/              # PC 端商城
├── docker-compose.yml   # ✅ Docker 编排（包含 MinIO）
├── .env.example         # ✅ 环境变量模板（包含 MinIO 配置）
├── start.sh / start.bat # ✅ 一键启动脚本
└── stop.sh / stop.bat   # ✅ 停止服务脚本
```

## 🎯 核心功能

### 1. 商品管理（✅ MinIO 多图支持）

- **多主图**: 最多 10 张，第一张为封面
- **详情图**: 最多 20 张，按顺序展示
- **MinIO 存储**: 图片存储在 MinIO，自动返回 URL
- **轮播展示**: 前端自动轮播主图

**API 示例:**

```bash
# 上传图片
curl -X POST http://localhost:8000/api/system/upload/image/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@product.jpg"

# 创建商品
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "price": 8999.00,
    "main_images": ["http://minio/img1.jpg", "http://minio/img2.jpg"],
    "detail_images": ["http://minio/detail1.jpg"]
  }'
```

### 2. MinIO 对象存储

- **单图上传**: `POST /api/system/upload/image/`
- **批量上传**: `POST /api/system/upload/images/` (最多 10 张)
- **自动存储桶**: 自动创建 `yph-products` 存储桶
- **公开访问**: 自动配置公开读取策略

### 3. 用户认证

- JWT Token 认证
- 微信小程序登录
- 手机号验证码登录
- OAuth 第三方登录

### 4. 订单系统

- 购物车管理
- 订单创建、支付、发货
- 订单状态跟踪
- 退款退货

### 5. 营销活动

- 优惠券系统
- 限时秒杀
- 拼团活动
- 积分商城

## 🔧 手动部署（高级）

如果不使用一键脚本，可以手动部署：

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，修改密码等配置
```

### 2. 启动服务

```bash
docker-compose up -d
```

### 3. 初始化数据库

```bash
# 等待 MySQL 启动（约 30 秒）
docker-compose exec backend python manage.py migrate

# 创建超级管理员
docker-compose exec backend python manage.py createsuperuser
```

### 4. 测试 MinIO

```bash
docker-compose exec backend python test_minio.py
```

## 📊 服务架构

```
┌─────────────────────────────────────────────────────────┐
│                     Nginx (80/443)                      │
│                    反向代理 + 静态文件                    │
└────────────┬───────────────────────────┬────────────────┘
             │                           │
    ┌────────▼────────┐         ┌────────▼─────────┐
    │  Frontend (Vue) │         │  Backend (Django)│
    │  Admin/H5/PC    │         │    REST API      │
    └─────────────────┘         └────────┬─────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
           ┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
           │  MySQL (3306)   │  │  Redis (6379)   │  │ MinIO (9000/1) │
           │     数据库       │  │      缓存        │  │   对象存储      │
           └─────────────────┘  └─────────────────┘  └────────────────┘
```

## ⚙️ 环境要求

- **Docker**: >= 20.10
- **Docker Compose**: >= 2.0
- **内存**: >= 4GB
- **磁盘**: >= 20GB

## 🔐 生产环境部署

生产环境部署前，**务必**修改以下配置：

### 1. 修改 .env 文件

```bash
# 数据库密码
MYSQL_ROOT_PASSWORD=your-secure-password-here
MYSQL_PASSWORD=your-secure-password-here

# Redis 密码
REDIS_PASSWORD=your-redis-password-here

# Django 密钥（使用随机字符串）
SECRET_KEY=your-random-long-secret-key-at-least-50-characters

# MinIO 密钥
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key-at-least-8-characters

# 域名配置
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
MINIO_PUBLIC_URL=https://cdn.yourdomain.com
```

### 2. 启用 HTTPS

```bash
# 申请 SSL 证书（Let's Encrypt）
# 配置 Nginx SSL
# 修改 MINIO_SECURE=True
```

### 3. 配置防火墙

```bash
# 只开放必要端口
ufw allow 80
ufw allow 443
ufw enable
```

## 📚 详细文档

| 文档 | 说明 |
|------|------|
| [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) | Docker 完整部署指南 |
| [backend/README_MINIO.md](backend/README_MINIO.md) | MinIO 快速开始 |
| [backend/docs/MINIO_INTEGRATION.md](backend/docs/MINIO_INTEGRATION.md) | MinIO 集成详解 |
| [backend/docs/PRODUCT_IMAGES.md](backend/docs/PRODUCT_IMAGES.md) | 产品图片管理 |
| [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md) | MinIO 集成总结 |

## 🆘 常见问题

### 服务无法启动？

```bash
# 检查端口占用
netstat -tuln | grep -E '3000|3001|8000|8080|9000|9001'

# 查看日志
docker-compose logs
```

### MinIO 连接失败？

```bash
# 检查 MinIO 状态
docker-compose ps minio

# 查看 MinIO 日志
docker-compose logs minio

# 重启 MinIO
docker-compose restart minio
```

### 数据库迁移失败？

```bash
# 删除容器和卷，重新开始
./stop.sh --clean
./start.sh
```

## 🎉 开始使用

现在你已经准备好了！尝试：

1. ✅ 访问管理后台 http://localhost:3000
2. ✅ 创建管理员账号
3. ✅ 上传产品图片到 MinIO
4. ✅ 创建第一个商品
5. ✅ 在 H5 端查看商品

**祝你使用愉快！** 🚀

---

**文档更新**: 2026-07-27  
**版本**: v1.0
