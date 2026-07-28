# 数据库迁移文件说明

## 📋 概述

本目录存放所有数据库结构变更的 SQL 脚本。

## 📝 命名规范

文件命名格式：`YYYYMMDD_description.sql`

例如：
- `20260727_add_user_avatar.sql` - 添加用户头像字段
- `20260727_modify_product_images.sql` - 修改产品图片字段

## 🚀 使用方法

### 1. 执行迁移脚本

**Docker 环境（推荐）:**

```bash
# 备份数据库
docker-compose exec mysql mysqldump -u yph -pyph123456 yph > backup_$(date +%Y%m%d).sql

# 执行迁移
docker-compose exec -T mysql mysql -u yph -pyph123456 yph < sql/migrations/20260727_modify_product_images.sql

# 验证结果
docker-compose exec mysql mysql -u yph -pyph123456 yph -e "DESC product;"

# 重启后端
docker-compose restart backend
```

**本地环境:**

```bash
# 备份数据库
mysqldump -u root -p yph > backup_$(date +%Y%m%d).sql

# 执行迁移
mysql -u root -p yph < sql/migrations/20260727_modify_product_images.sql

# 验证结果
mysql -u root -p yph -e "DESC product;"
```

### 2. 创建新的迁移脚本

参考现有脚本格式，包含：

1. **文件头注释** - 说明变更内容、日期、原因
2. **事务包裹** - 使用 START TRANSACTION 和 COMMIT
3. **执行说明** - 详细的执行步骤
4. **回滚方案**（可选） - 如何撤销变更

**模板:**

```sql
-- ===================================================================
-- 变更说明
-- 创建日期: YYYY-MM-DD
-- 说明: 详细描述变更内容
-- ===================================================================

START TRANSACTION;

-- 在这里写 SQL 语句
ALTER TABLE `table_name` ADD COLUMN `field_name` VARCHAR(255) DEFAULT NULL COMMENT '字段说明';

COMMIT;

-- ===================================================================
-- 执行说明:
-- 1. 备份数据库
-- 2. 执行迁移
-- 3. 验证结果
-- ===================================================================
```

## 📂 现有迁移文件

| 文件 | 日期 | 说明 |
|------|------|------|
| `20260727_modify_product_images.sql` | 2026-07-27 | 产品表支持 MinIO 多图存储 |

## ⚠️ 重要提示

1. **必须备份** - 执行任何迁移前，务必先备份数据库
2. **测试环境** - 先在测试环境验证，确认无误后再在生产环境执行
3. **事务控制** - 使用事务确保数据一致性
4. **记录变更** - 更新本 README 文件记录所有迁移
5. **同步 Models** - 执行 SQL 后，同步更新 Django models.py

## 🔄 迁移流程

```
1. 编写 SQL 迁移脚本
   ↓
2. 备份生产数据库
   ↓
3. 在测试环境执行并验证
   ↓
4. 在生产环境执行
   ↓
5. 更新 Django models.py
   ↓
6. 重启应用服务
   ↓
7. 验证功能正常
```

## 🆘 回滚方案

如果迁移出现问题：

```bash
# 1. 停止应用
docker-compose stop backend

# 2. 恢复数据库备份
docker-compose exec -T mysql mysql -u yph -pyph123456 yph < backup_YYYYMMDD.sql

# 3. 重启应用
docker-compose restart backend
```

## 📚 参考

- MySQL ALTER TABLE: https://dev.mysql.com/doc/refman/8.0/en/alter-table.html
- MySQL JSON 数据类型: https://dev.mysql.com/doc/refman/8.0/en/json.html
- 事务控制: https://dev.mysql.com/doc/refman/8.0/en/commit.html
