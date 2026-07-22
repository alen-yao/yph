# YPH 电商系统

<div align="center">

**🎉 一个功能完整的现代化电商系统 🎉**

结合 **Dailyfresh-B2C** 的简洁Python后端架构 + **ModulithShop** 的完整业务功能

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.4-brightgreen.svg)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📖 项目简介

YPH 是一个基于 **Python Django + Vue3** 的现代化B2C电商系统，完美融合了两个优秀开源项目的优点：

- ✅ **后端架构** - 参照 Dailyfresh-B2C，使用 Python + Django + DRF，代码简洁高效
- ✅ **业务功能** - 参照 ModulithShop，功能完整，涵盖电商核心业务场景
- ✅ **前端设计** - 参照 ModulithShop 风格，界面美观易用
- ✅ **Docker 部署** - 一键启动，开箱即用

## 🎯 核心特性

### 后端技术栈
- **Python 3.11+** & **Django 4.2**
- **Django REST Framework** - RESTful API
- **JWT** 认证 - 安全的Token认证
- **MySQL 8.0** - 数据存储
- **Redis 7** - 缓存和Session
- **Celery** - 异步任务处理
- **Swagger** - 自动API文档
- **Docker** - 容器化部署

### 前端技术栈
- **Vue 3** + **Vite** - 现代化构建工具
- **Element Plus** - 管理后台UI组件库
- **Vant 4** - 移动端UI组件库
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP客户端

## 📦 项目结构

```
yph/
├── backend/                    # Django 后端
│   ├── apps/                  # 业务模块
│   │   ├── users/            # 用户模块 ✅
│   │   ├── products/         # 商品模块 ✅
│   │   ├── trade/            # 交易模块 ✅
│   │   ├── marketing/        # 营销模块 ✅
│   │   ├── payment/          # 支付模块 ✅
│   │   ├── shops/            # 店铺模块 ✅
│   │   └── system/           # 系统模块 ✅
│   ├── yph/                  # 项目配置
│   ├── requirements.txt      # Python依赖
│   └── Dockerfile           # Docker镜像
├── frontend/                  # 前端项目
│   ├── admin/               # Vue3 管理后台 ✅
│   ├── h5/                  # H5 移动端商城 ✅
│   └── pc/                  # PC 端商城 ✅
├── sql/                       # SQL脚本
│   ├── init.sql             # 数据库初始化脚本
│   ├── migrations/          # 数据库变更记录
│   └── README.md            # SQL 管理文档
├── nginx/                     # Nginx 配置
├── docker-compose.yml        # Docker Compose 配置
├── add-field.sh             # 快速添加字段脚本
└── README.md                # 项目说明（本文件）
```

---

## ⚡ 快速开始

### 方式一：Docker Compose（推荐）

#### 环境要求
- Docker
- Docker Compose

#### 一键启动
```bash
# 1. 克隆项目
git clone <your-repository-url>
cd yph

# 2. 启动所有服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

#### 访问地址
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/api/docs/
- **管理后台**: http://localhost:3000
- **H5 商城**: http://localhost:3001
- **PC 商城**: http://localhost:8080

**首次启动等待约 30-60 秒，数据库会自动初始化。**

---

### 方式二：本地开发环境

#### 环境要求
- Python 3.11+
- MySQL 8.0+
- Redis 7+
- Node.js 18+

#### 1️⃣ 数据库初始化

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE yph CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入初始化脚本
mysql -u root -p yph < sql/init.sql
```

#### 2️⃣ 后端启动

```bash
# 安装依赖
cd backend
pip install -r requirements.txt

# 配置环境变量（创建 .env 文件）
cp .env.example .env  # 根据需要修改配置

# 收集静态文件
python manage.py collectstatic --noinput

# 启动服务
python manage.py runserver 0.0.0.0:8000
```

#### 3️⃣ 管理后台启动

```bash
cd frontend/admin
npm install
npm run dev  # http://localhost:3000
```

#### 4️⃣ H5 商城启动

```bash
cd frontend/h5
npm install
npm run dev  # http://localhost:3001
```

#### 5️⃣ PC 商城启动

```bash
cd frontend/pc
npm install
npm run dev  # http://localhost:8080
```

---

## 🎨 功能模块

### 用户模块 (users)
- ✅ 用户注册/登录（JWT认证、多端登录支持）
- ✅ 用户信息管理
- ✅ 收货地址管理
- ✅ 用户等级系统
- ✅ 积分系统
- ✅ 消息通知
- ✅ 登录历史

**多端登录说明**：
- 支持 PC、H5、小程序等多端同时登录
- 每个端独立的 Token 管理
- 设备信息记录和管理

### 商品模块 (products)
- ✅ 商品分类管理（支持多级分类）
- ✅ 品牌管理
- ✅ 商品基础信息
- ✅ 商品SKU管理
- ✅ 商品规格管理
- ✅ 商品评论系统
- ✅ 商品标签

### 交易模块 (trade)
- ✅ 购物车管理
- ✅ 订单创建
- ✅ 订单状态流转
- ✅ 退货/退款管理
- ✅ 物流跟踪

### 营销模块 (marketing)
- ✅ 营销活动管理
- ✅ 优惠券系统
- ✅ 限时秒杀
- ✅ 拼团活动
- ✅ 砍价活动

### 支付模块 (payment)
- ✅ 微信支付（接口预留）
- ✅ 支付宝支付（接口预留）
- ✅ 余额支付
- ✅ 支付回调处理

### 店铺模块 (shops)
- ✅ 商品收藏
- ✅ 浏览历史
- ✅ 搜索历史

### 系统模块 (system)
- ✅ 系统配置
- ✅ 轮播图管理
- ✅ 角色权限管理

---

## 🛠️ 开发指南

### 数据库管理

本项目**不使用 Django migrations**，采用 **SQL 文件管理**数据库结构，更简单、更稳定。

#### 添加新字段

**方式 1：使用脚本（推荐）**

```bash
./add-field.sh
```

根据提示输入信息：
- 表名：`user`
- 字段名：`avatar_url`
- 字段类型：选择 `2` (VARCHAR(255))
- 默认值：留空
- 说明：`头像URL`

脚本会自动：
1. 执行 SQL 添加字段
2. 保存 SQL 到 `sql/migrations/`
3. 提示修改 models.py

**方式 2：手动执行 SQL**

```bash
# 1. 创建 SQL 文件
# sql/migrations/20260722_add_user_avatar.sql
ALTER TABLE `user` ADD COLUMN `avatar_url` VARCHAR(255) DEFAULT NULL COMMENT '头像URL';

# 2. 执行 SQL
docker-compose exec mysql mysql -u yph -pyph123456 -D yph < sql/migrations/20260722_add_user_avatar.sql

# 3. 修改 models.py
# backend/apps/users/models.py
class User(AbstractUser):
    avatar_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='头像URL')

# 4. 重启后端
docker-compose restart backend
```

详细说明见 [sql/README.md](sql/README.md)

### 创建超级用户

```bash
# Docker 环境
docker-compose exec backend python manage.py createsuperuser

# 本地环境
cd backend
python manage.py createsuperuser
```

### 查看日志

```bash
# 查看所有日志
docker-compose logs -f

# 查看指定服务日志
docker-compose logs -f backend
docker-compose logs -f mysql
docker-compose logs -f redis
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库
docker-compose exec mysql mysql -u yph -pyph123456 -D yph

# 执行 Django 命令
docker-compose exec backend python manage.py shell
```

---

## 🔧 常用命令

### Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看服务状态
docker-compose ps

# 重启服务
docker-compose restart [service-name]

# 查看日志
docker-compose logs -f [service-name]

# 重新构建
docker-compose build [service-name]

# 完全重置（删除所有数据）
docker-compose down -v
```

### 数据库操作

```bash
# 备份数据库
docker-compose exec mysql mysqldump -u yph -pyph123456 yph > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker-compose exec -T mysql mysql -u yph -pyph123456 yph < backup_20260722.sql

# 查看所有表
docker-compose exec mysql mysql -u yph -pyph123456 -D yph -e "SHOW TABLES;"

# 查看表结构
docker-compose exec mysql mysql -u yph -pyph123456 -D yph -e "DESC user;"

# 查询数据
docker-compose exec mysql mysql -u yph -pyph123456 -D yph -e "SELECT * FROM user LIMIT 10;"
```

---

## 📊 API文档

启动后端服务后，访问以下地址查看完整API文档：

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

### 主要API端点

| 模块 | 端点 | 说明 |
|-----|------|-----|
| 用户 | `/api/v1/users/` | 用户注册、登录、信息管理 |
| 商品 | `/api/v1/products/` | 商品分类、品牌、SKU |
| 交易 | `/api/v1/trade/` | 订单、购物车 |
| 营销 | `/api/v1/marketing/` | 优惠券、活动 |
| 支付 | `/api/v1/payment/` | 支付、退款 |

### API 认证

使用 JWT Token 认证：

```bash
# 1. 登录获取 Token
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 2. 使用 Token 访问接口
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer <your-token>"
```

---

## 🚀 部署指南

### 生产环境部署建议

#### 1. 环境变量配置

创建 `.env` 文件：

```bash
# 数据库配置
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_DATABASE=yph
MYSQL_USER=yph
MYSQL_PASSWORD=your_secure_password

# Redis 配置
REDIS_PASSWORD=your_redis_password

# Django 配置
DEBUG=False
SECRET_KEY=your_secret_key_here_at_least_50_characters_long
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# 端口配置（可选）
BACKEND_PORT=8000
ADMIN_PORT=3000
H5_PORT=3001
PC_PORT=8080
```

#### 2. 使用外部数据库

不要在生产环境用 Docker 运行数据库，使用云数据库服务：

- 阿里云 RDS
- AWS RDS
- 腾讯云 TencentDB

修改 `docker-compose.yml`：

```yaml
backend:
  environment:
    - DATABASE_HOST=your-rds-host.com
    - DATABASE_PORT=3306
    - DATABASE_NAME=yph
    - DATABASE_USER=yph
    - DATABASE_PASSWORD=your_password
```

#### 3. HTTPS 配置

使用 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 4. 性能优化

- **启用 Redis 缓存**
- **配置 CDN 加速静态资源**
- **调整 Gunicorn workers 数量**（CPU 核心数 × 2 + 1）
- **启用 Gzip 压缩**
- **优化数据库查询索引**

#### 5. 监控告警

- 使用 Prometheus + Grafana 监控服务
- 配置日志收集（ELK Stack）
- 设置告警规则（CPU、内存、磁盘）

#### 6. 定期备份

```bash
# 创建备份脚本 backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec mysql mysqldump -u yph -pyph123456 yph > /backup/yph_$DATE.sql
# 上传到云存储
aws s3 cp /backup/yph_$DATE.sql s3://your-bucket/

# 设置定时任务
crontab -e
0 2 * * * /path/to/backup.sh
```

---

## 🐛 常见问题

### 1. 端口被占用

```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "8001:8000"  # 改成其他端口
```

### 2. 数据库连接失败

```bash
# 查看 MySQL 日志
docker-compose logs mysql

# 确认 MySQL 已启动并健康
docker-compose ps mysql

# 等待 MySQL 完全启动（约30秒）
docker-compose logs mysql | grep "ready for connections"
```

### 3. 前端无法访问后端

检查 `frontend/*/vite.config.js` 中的代理配置：

```javascript
// Docker 环境
proxy: {
  '/api': {
    target: 'http://backend:8000',
    changeOrigin: true,
  }
}

// 本地环境
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

### 4. 静态文件 404

```bash
# 重新收集静态文件
docker-compose exec backend python manage.py collectstatic --noinput --clear

# 检查静态文件目录
docker-compose exec backend ls -la /app/static/
```

### 5. 完全重置环境

```bash
# ⚠️ 警告：此操作会删除所有数据！
docker-compose down -v  # 删除所有容器和数据卷
docker-compose up -d    # 重新启动
```

---

## 📈 性能对比

| 对比项 | ModulithShop (Java) | YPH (Python) |
|-------|---------------------|--------------|
| 语言 | Java | Python ✅ |
| 代码量 | 多 | 少 ✅ |
| 学习曲线 | 陡峭 | 平缓 ✅ |
| 开发效率 | 中 | 高 ✅ |
| 部署难度 | 复杂（需JVM） | 简单 ✅ |
| 内存占用 | 高（JVM 500MB+） | 低（100MB+） ✅ |
| 启动速度 | 慢（30s+） | 快（5s） ✅ |
| 业务功能 | 完整 ✅ | 完整 ✅ |

### 核心亮点

1. **🚀 简洁高效** - Python + Django，代码简洁易维护
2. **📦 功能完整** - 参照成熟商业项目，业务功能齐全
3. **🎨 界面美观** - 参照 ModulithShop 前端设计，美观易用
4. **📖 文档完善** - Swagger 自动文档，部署文档齐全
5. **🔐 安全可靠** - JWT 认证，权限管理完善
6. **⚡ 易于部署** - Docker 一键启动，不需要 JVM
7. **🛠️ 易于维护** - SQL 文件管理数据库，清晰可控

---

## 🤝 参考项目

- [Dailyfresh-B2C](https://github.com/Dailyfresh-B2C) - 后端架构参考
- [ModulithShop](https://github.com/shsuishang/modulithshop) - 业务功能参考

---

## 📝 开源协议

本项目采用 [MIT](LICENSE) 开源协议

---

## 🙏 致谢

感谢以下开源项目：
- Django & Django REST Framework
- Vue.js & Element Plus & Vant
- Dailyfresh-B2C
- ModulithShop

---

## 📧 联系方式

如有问题或建议，欢迎提交 Issue

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star ⭐**

Made with ❤️ by YPH Team

</div>
