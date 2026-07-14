# YPH 电商系统 - 快速启动指南

## 🚀 5分钟快速启动

### 前置准备

确保已安装以下软件：
- ✅ Python 3.8+
- ✅ MySQL 8.0+
- ✅ Redis 5.0+
- ✅ Node.js 16+

---

## 方式一：一键启动（推荐）

### Windows 系统

```bash
# 1. 启动MySQL和Redis服务

# 2. 启动后端
cd backend
start.bat

# 3. 新开命令行窗口，启动管理后台
cd frontend/admin
npm install && npm run dev

# 4. 新开命令行窗口，启动H5商城
cd frontend/h5
npm install && npm run dev
```

### Linux/Mac 系统

```bash
# 1. 启动MySQL和Redis服务
brew services start mysql
brew services start redis

# 2. 启动后端
cd backend
chmod +x start.sh
./start.sh

# 3. 新开终端，启动管理后台
cd frontend/admin
npm install && npm run dev

# 4. 新开终端，启动H5商城
cd frontend/h5
npm install && npm run dev
```

---

## 方式二：手动启动

### 第一步：数据库准备

```sql
-- 1. 登录MySQL
mysql -u root -p

-- 2. 创建数据库
CREATE DATABASE yph_ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. 退出
exit;
```

### 第二步：后端启动

```bash
cd backend

# 1. 创建虚拟环境（可选）
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 修改数据库配置（如需要）
# 编辑 yph/settings.py 中的数据库配置

# 4. 执行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 5. 导入初始数据
mysql -u root -p yph_ecommerce < ../sql/init_database.sql

# 6. 创建超级用户
python manage.py createsuperuser
# 按提示输入用户名、邮箱和密码

# 7. 启动服务
python manage.py runserver
```

**后端已启动!** 访问:
- API文档: http://localhost:8000/api/docs/
- 管理后台: http://localhost:8000/admin/

### 第三步：管理后台启动

```bash
# 新开终端
cd frontend/admin

# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm run dev
```

**管理后台已启动!** 访问: http://localhost:3000

默认登录信息:
- 用户名: admin
- 密码: admin123

### 第四步：H5商城启动

```bash
# 新开终端
cd frontend/h5

# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm run dev
```

**H5商城已启动!** 访问: http://localhost:3001

---

## 📋 验证安装

### 1. 检查后端

访问 http://localhost:8000/api/docs/

如果能看到Swagger API文档页面，说明后端启动成功！

### 2. 检查管理后台

访问 http://localhost:3000

使用 `admin / admin123` 登录，如果能看到管理后台首页，说明成功！

### 3. 检查H5商城

访问 http://localhost:3001

如果能看到商城首页，说明成功！

---

## 🎯 常见问题

### Q1: 数据库连接失败？
**A:** 检查以下几点：
1. MySQL服务是否启动
2. 数据库是否创建
3. `yph/settings.py` 中的数据库配置是否正确

### Q2: Redis连接失败？
**A:** 检查Redis服务是否启动
```bash
# Windows
redis-server

# Linux/Mac
redis-server
# 或
brew services start redis
```

### Q3: npm install 失败？
**A:** 尝试使用国内镜像
```bash
npm install --registry=https://registry.npmmirror.com
```

### Q4: 端口被占用？
**A:** 修改端口配置
- 后端: `python manage.py runserver 8001`
- 管理后台: 修改 `frontend/admin/vite.config.js` 中的 `port`
- H5商城: 修改 `frontend/h5/vite.config.js` 中的 `port`

---

## 🎉 启动成功!

现在你可以：

1. **浏览API文档**: http://localhost:8000/api/docs/
2. **登录管理后台**: http://localhost:3000
3. **体验H5商城**: http://localhost:3001

## 📚 下一步

- 查看 [API文档](docs/API文档.md) 了解接口使用
- 查看 [部署文档](docs/部署文档.md) 了解生产环境部署
- 查看 [项目总结](docs/项目总结.md) 了解项目架构

---

祝你使用愉快！ 🎈
