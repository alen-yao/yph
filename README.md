# YPH 电商系统

<div align="center">

**🎉 一个功能完整的现代化电商系统 🎉**

结合 **Dailyfresh-B2C** 的简洁Python后端架构 + **ModulithShop** 的完整业务功能

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.4-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📖 项目简介

YPH 是一个基于 **Python Django + Vue3** 的现代化B2C电商系统，完美融合了两个优秀开源项目的优点：

- ✅ **后端架构** - 参照 Dailyfresh-B2C，使用 Python + Django + DRF，代码简洁高效
- ✅ **业务功能** - 参照 ModulithShop，功能完整，涵盖电商核心业务场景
- ✅ **前端设计** - 参照 ModulithShop 风格，界面美观易用

## 🎯 核心特性

### 后端技术栈
- **Python 3.8+** & **Django 4.2**
- **Django REST Framework** - RESTful API
- **JWT** 认证 - 安全的Token认证
- **MySQL 8.0** - 数据存储
- **Redis** - 缓存和Session
- **Swagger** - 自动API文档

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
│   ├── start.bat            # Windows启动脚本
│   └── start.sh             # Linux/Mac启动脚本
├── frontend/                  # 前端项目
│   ├── admin/               # Vue3 管理后台 ✅
│   └── h5/                  # H5 移动端商城 ✅
├── docs/                      # 项目文档
├── sql/                       # SQL脚本
└── README.md                 # 项目说明
```

## ⚡ 快速开始

### 环境要求

- Python 3.8+
- MySQL 8.0+
- Redis 5.0+
- Node.js 16+
- npm 8+

### 1️⃣ 后端启动

#### Windows:
```bash
cd backend
start.bat
```

#### Linux/Mac:
```bash
cd backend
chmod +x start.sh
./start.sh
```

#### 手动启动:
```bash
# 1. 创建数据库
mysql -u root -p
CREATE DATABASE yph_ecommerce CHARACTER SET utf8mb4;

# 2. 安装依赖
cd backend
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 4. 导入初始数据
mysql -u root -p yph_ecommerce < ../sql/init_database.sql

# 5. 创建超级用户
python manage.py createsuperuser

# 6. 启动服务
python manage.py runserver
```

**后端访问地址:**
- API文档: http://localhost:8000/api/docs/
- 管理后台: http://localhost:8000/admin/

### 2️⃣ 管理后台启动

```bash
cd frontend/admin
npm install
npm run dev
```

**访问地址:** http://localhost:3000

**默认账号:** admin / admin123

### 3️⃣ H5商城启动

```bash
cd frontend/h5
npm install
npm run dev
```

**访问地址:** http://localhost:3001

## 🎨 功能模块

### 用户模块 (users)
- ✅ 用户注册/登录 (JWT认证)
- ✅ 用户信息管理
- ✅ 收货地址管理
- ✅ 用户等级系统
- ✅ 积分系统
- ✅ 消息通知
- ✅ 登录历史

### 商品模块 (products)
- ✅ 商品分类管理（多级分类）
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
- ✅ 权限管理（Django内置）

## 📊 API文档

启动后端服务后，访问以下地址查看完整API文档：

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/

### 主要API端点

| 模块 | 端点 | 说明 |
|-----|------|-----|
| 用户 | `/api/v1/users/` | 用户相关接口 |
| 商品 | `/api/v1/products/` | 商品相关接口 |
| 交易 | `/api/v1/trade/` | 订单、购物车接口 |
| 营销 | `/api/v1/marketing/` | 营销活动接口 |
| 支付 | `/api/v1/payment/` | 支付相关接口 |

## 🖥️ 管理后台功能

- ✅ 数据概览（Dashboard）
- ✅ 商品管理
- ✅ 订单管理
- ✅ 用户管理
- ✅ 营销活动
- ✅ 系统设置

## 📱 H5移动端功能

- ✅ 首页（轮播图、分类导航、商品列表）
- ✅ 商品分类
- ✅ 商品详情
- ✅ 购物车
- ✅ 用户中心
- ✅ 订单管理

## 📚 项目文档

- [API文档](docs/API文档.md)
- [部署文档](docs/部署文档.md)
- [项目总结](docs/项目总结.md)

## 🔧 开发说明

### 后端开发

```bash
# 创建新的app
python manage.py startapp app_name

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 前端开发

```bash
# 管理后台
cd frontend/admin
npm run dev

# H5商城
cd frontend/h5
npm run dev
```

## 📈 功能对比

| 功能模块 | ModulithShop (Java) | YPH (Python) | 完成度 |
|---------|---------------------|--------------|--------|
| 用户管理 | ✅ | ✅ | 100% |
| 商品管理 | ✅ | ✅ | 100% |
| 订单管理 | ✅ | ✅ | 100% |
| 购物车 | ✅ | ✅ | 100% |
| 支付集成 | ✅ | ✅ | 80% |
| 营销活动 | ✅ | ✅ | 90% |
| 店铺管理 | ✅ | ✅ | 90% |

## 🎯 优势特点

### vs ModulithShop (Java版)

| 对比项 | ModulithShop | YPH |
|-------|--------------|-----|
| 语言 | Java | Python ✅ |
| 代码量 | 多 | 少 ✅ |
| 学习曲线 | 陡峭 | 平缓 ✅ |
| 开发效率 | 中 | 高 ✅ |
| 部署难度 | 复杂(需JVM) | 简单 ✅ |
| 业务功能 | 完整 ✅ | 完整 ✅ |

### 核心亮点

1. **🚀 简洁高效** - Python + Django，代码简洁易维护
2. **📦 功能完整** - 参照成熟商业项目，业务功能齐全
3. **🎨 界面美观** - 参照ModulithShop前端设计，美观易用
4. **📖 文档完善** - Swagger自动文档，部署文档齐全
5. **🔐 安全可靠** - JWT认证，权限管理完善
6. **⚡ 易于部署** - 不需要JVM，部署简单

## 🤝 参考项目

- [Dailyfresh-B2C](https://github.com/Dailyfresh-B2C) - 后端架构参考
- [ModulithShop](https://github.com/shsuishang/modulithshop) - 业务功能参考

## 📝 开源协议

本项目采用 [MIT](LICENSE) 开源协议

## 🙏 致谢

感谢以下开源项目：
- Django & Django REST Framework
- Vue.js & Element Plus & Vant
- Dailyfresh-B2C
- ModulithShop

## 📧 联系方式

如有问题或建议，欢迎提交 Issue

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star ⭐**

Made with ❤️ by YPH Team

</div>
