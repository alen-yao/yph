# 🔄 产品表迁移指南 - MinIO 多图支持

## 📋 变更概述

为了支持 MinIO 对象存储和电商多图展示，产品表进行了以下变更：

### 旧字段（将被删除）
- `main_image` (ImageField) - 单张主图
- `images` (TextField) - 图片列表（JSON 字符串）
- `detail_html` (TextField) - 详情 HTML（可选保留）

### 新字段（已添加）
- `main_images` (JSON) - 主图列表，第一张为封面图
- `detail_images` (JSON) - 详情图列表，按顺序展示

## 🚀 迁移步骤

### 步骤 1: 备份数据库（重要！）

```bash
# Docker 环境
docker-compose exec mysql mysqldump -u yph -pyph123456 yph > backup_$(date +%Y%m%d_%H%M%S).sql

# 本地环境
mysqldump -u root -p yph > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 步骤 2: 检查当前表结构

```bash
# 查看 product 表结构
docker-compose exec mysql mysql -u yph -pyph123456 yph -e "DESCRIBE product;"

# 查看现有数据
docker-compose exec mysql mysql -u yph -pyph123456 yph -e "SELECT id, name, main_image, images FROM product LIMIT 5;"
```

### 步骤 3: 执行迁移 SQL

```bash
# 执行迁移脚本
docker-compose exec -T mysql mysql -u yph -pyph123456 yph < sql/migrations/20260727_modify_product_images.sql
```

**脚本会自动完成：**
1. ✅ 添加 `main_images` 字段（JSON 类型）
2. ✅ 添加 `detail_images` 字段（JSON 类型）
3. ✅ 迁移旧数据（如果存在）
4. ⚠️ 删除旧字段（默认注释掉，需手动取消注释）

### 步骤 4: 验证迁移结果

```bash
# 查看新表结构
docker-compose exec mysql mysql -u yph -pyph123456 yph -e "DESCRIBE product;"

# 查看迁移后的数据
docker-compose exec mysql mysql -u yph -pyph123456 yph -e "SELECT id, name, main_images, detail_images FROM product LIMIT 5;"

# 验证 JSON 格式
docker-compose exec mysql mysql -u yph -pyph123456 yph -e "SELECT id, JSON_LENGTH(main_images) as main_count, JSON_LENGTH(detail_images) as detail_count FROM product WHERE main_images IS NOT NULL LIMIT 5;"
```

### 步骤 5: 重启后端服务

```bash
# 重启后端容器
docker-compose restart backend

# 查看日志确认启动成功
docker-compose logs -f backend
```

### 步骤 6: 测试功能

```bash
# 测试 MinIO 连接
docker-compose exec backend python test_minio.py

# 创建测试数据
docker-compose exec backend python scripts/migrate_product_images.py --sample
```

## 📊 数据迁移详情

### 迁移逻辑

```sql
-- 旧数据示例
main_image: 'products/main/abc123.jpg'
images: '["img1.jpg", "img2.jpg"]'

-- 迁移后
main_images: ["http://localhost:9000/yph-products/products/main/abc123.jpg"]
detail_images: []
```

### 手动数据迁移（如需要）

如果自动迁移不符合你的需求，可以手动执行：

```sql
-- 示例：将本地路径转换为 MinIO URL
UPDATE product 
SET main_images = JSON_ARRAY(
    CONCAT('http://localhost:9000/yph-products/', main_image)
)
WHERE main_image IS NOT NULL;

-- 示例：从 images 字段迁移到 detail_images
UPDATE product 
SET detail_images = images
WHERE images IS NOT NULL AND JSON_VALID(images);
```

## ⚠️ 注意事项

### 1. 旧字段处理

迁移脚本**默认不删除**旧字段，给你时间验证。验证无误后，手动删除：

```sql
-- 确认数据迁移正确后，执行以下语句
ALTER TABLE product DROP COLUMN main_image;
ALTER TABLE product DROP COLUMN images;
```

### 2. 图片路径转换

如果你的旧图片不在 MinIO，需要：
1. 将旧图片上传到 MinIO
2. 获取新的 MinIO URL
3. 更新 `main_images` 和 `detail_images` 字段

### 3. Django Models 已更新

Product 模型已更新，无需手动修改：
- [backend/apps/products/models.py](backend/apps/products/models.py#L73-L76)

### 4. 序列化器已更新

ProductSerializer 已支持新字段：
- [backend/apps/products/serializers.py](backend/apps/products/serializers.py)

## 🔙 回滚方案

如果需要回滚迁移：

### 方案 1: 恢复数据库备份

```bash
# 停止后端
docker-compose stop backend

# 恢复备份
docker-compose exec -T mysql mysql -u yph -pyph123456 yph < backup_YYYYMMDD_HHMMSS.sql

# 重启服务
docker-compose restart backend
```

### 方案 2: 手动回滚（如果只添加了字段）

```sql
-- 删除新字段
ALTER TABLE product DROP COLUMN main_images;
ALTER TABLE product DROP COLUMN detail_images;
```

## 📝 检查清单

在执行迁移前，确认以下事项：

- [ ] 已备份数据库
- [ ] 已在测试环境验证
- [ ] 已停止相关的定时任务
- [ ] 已通知团队成员
- [ ] 已准备好回滚方案
- [ ] 已更新相关文档

在迁移完成后，确认：

- [ ] 表结构正确
- [ ] 数据已正确迁移
- [ ] 后端服务正常启动
- [ ] API 接口正常工作
- [ ] 前端页面正常显示
- [ ] MinIO 图片可正常访问

## 🆘 常见问题

### Q: 执行 SQL 报错 "Unknown column 'main_image'"

A: 说明表中不存在 `main_image` 字段，注释掉迁移脚本中的数据迁移部分即可。

### Q: JSON 字段显示为 NULL

A: 正常现象，新创建的记录默认为 NULL。上传图片后会自动填充。

### Q: 需要保留旧字段吗？

A: 建议先保留，验证无误后再删除。如果你的旧数据很重要，可以永久保留作为备份。

### Q: 如何批量上传旧图片到 MinIO？

A: 可以编写脚本批量上传，参考 [backend/scripts/migrate_product_images.py](backend/scripts/migrate_product_images.py)

## 📚 相关文档

- [MinIO 集成文档](backend/docs/MINIO_INTEGRATION.md)
- [产品图片管理](backend/docs/PRODUCT_IMAGES.md)
- [数据库迁移说明](sql/migrations/README.md)
- [产品模型升级说明](backend/PRODUCT_MODEL_UPGRADE.md)

---

**迁移日期**: 2026-07-27  
**版本**: v1.0
