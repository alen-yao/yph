# 数据库管理说明

本项目**不使用 Django migrations**，改为手动管理数据库表结构。

## 📁 文件说明

- `init.sql` - 数据库初始化脚本（创建所有表）
- `migrations/` - 存放所有数据库变更 SQL（按日期命名）

## 🚀 初始化数据库

```bash
# 完全重置数据库
docker-compose down -v
docker-compose up -d

# init.sql 会在 MySQL 容器启动时自动执行
```

## ➕ 添加新字段

### 步骤 1：修改 models.py

```python
# backend/apps/users/models.py
class User(AbstractUser):
    mobile = models.CharField(max_length=11)
    new_field = models.CharField(max_length=50, default='')  # ← 添加新字段
```

### 步骤 2：创建迁移 SQL

创建文件 `sql/migrations/20260722_add_user_new_field.sql`：

```sql
-- 添加 user 表的 new_field 字段
-- 日期: 2026-07-22
-- 作者: YourName

ALTER TABLE `user` 
ADD COLUMN `new_field` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '新字段说明';
```

### 步骤 3：执行 SQL

```bash
# 方式1：进入数据库执行（推荐）
docker-compose exec mysql mysql -u yph -pyph123456 -D yph < sql/migrations/20260722_add_user_new_field.sql

# 方式2：直接执行 SQL 语句
docker-compose exec mysql mysql -u yph -pyph123456 -D yph -e "
ALTER TABLE user ADD COLUMN new_field VARCHAR(50) NOT NULL DEFAULT '';
"
```

### 步骤 4：重启后端

```bash
docker-compose restart backend
```

## 🔧 常用 SQL 模板

### 添加字段
```sql
ALTER TABLE `table_name` 
ADD COLUMN `field_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '字段说明';
```

### 修改字段
```sql
ALTER TABLE `table_name` 
MODIFY COLUMN `field_name` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '修改后的说明';
```

### 删除字段
```sql
ALTER TABLE `table_name` 
DROP COLUMN `field_name`;
```

### 添加索引
```sql
ALTER TABLE `table_name` 
ADD INDEX `idx_field_name` (`field_name`);
```

### 添加外键
```sql
ALTER TABLE `table_name` 
ADD CONSTRAINT `fk_table_name_field` 
FOREIGN KEY (`field_id`) REFERENCES `other_table` (`id`) ON DELETE CASCADE;
```

## 📝 迁移文件命名规范

格式：`YYYYMMDD_description.sql`

示例：
- `20260722_add_user_new_field.sql`
- `20260723_create_product_index.sql`
- `20260724_modify_order_status.sql`

## ⚠️ 注意事项

1. **每次修改数据库前先备份**
   ```bash
   docker-compose exec mysql mysqldump -u yph -pyph123456 yph > backup_$(date +%Y%m%d).sql
   ```

2. **测试 SQL 语句**
   - 先在本地测试，确认无误后再在生产环境执行

3. **记录所有变更**
   - 所有 SQL 变更都保存到 `sql/migrations/` 目录
   - 方便团队其他成员同步数据库结构

4. **如果需要完全重置数据库**
   ```bash
   docker-compose down -v  # 删除数据卷
   docker-compose up -d    # 重新创建，自动执行 init.sql
   ```

## 🎯 优点

✅ 不需要处理 Django migrations 的复杂性  
✅ 完全掌控数据库结构  
✅ 添加字段只需一条 SQL  
✅ 不会有迁移文件冲突问题  
✅ 团队协作更简单

## ❌ 缺点

❌ 需要手动写 SQL（但很简单）  
❌ 没有自动版本管理（但我们用 git 管理 SQL 文件）  
❌ 需要记住执行 SQL
