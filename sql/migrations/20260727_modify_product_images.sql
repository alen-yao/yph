-- ===================================================================
-- 产品表图片字段迁移 - 支持 MinIO 多图存储
-- 创建日期: 2026-07-27
-- 说明:
--   1. 删除旧的 main_image (ImageField) 和 images (TextField) 字段
--   2. 添加 main_images (JSON) 和 detail_images (JSON) 字段
--   3. main_images: 主图列表，第一张为封面图
--   4. detail_images: 详情图列表，按顺序展示
-- ===================================================================

-- 开始事务
START TRANSACTION;

-- 1. 添加新字段
-- 主图列表（JSON 格式）
ALTER TABLE `product` ADD COLUMN `main_images` JSON DEFAULT NULL COMMENT '主图列表(JSON数组)，第一张为封面图';

-- 详情图列表（JSON 格式）
ALTER TABLE `product` ADD COLUMN `detail_images` JSON DEFAULT NULL COMMENT '详情图列表(JSON数组)，按顺序展示';

-- 2. 数据迁移（如果有旧数据）
-- 如果 main_image 字段存在且有数据，迁移到 main_images
-- 注意：需要根据实际情况调整路径前缀
UPDATE `product`
SET `main_images` = JSON_ARRAY(CONCAT('http://localhost:9000/yph-products/', `main_image`))
WHERE `main_image` IS NOT NULL AND `main_image` != '';

-- 如果 images 字段存在且有数据，尝试迁移
-- 注意：这里假设 images 是 JSON 格式的字符串
-- 如果不是，需要根据实际情况调整
-- UPDATE `product`
-- SET `detail_images` = `images`
-- WHERE `images` IS NOT NULL AND `images` != '';

-- 3. 删除旧字段（可选，建议先备份数据）
-- 警告：执行前请确保数据已正确迁移！
-- ALTER TABLE `product` DROP COLUMN `main_image`;
-- ALTER TABLE `product` DROP COLUMN `images`;
-- ALTER TABLE `product` DROP COLUMN `detail_html`;

-- 提交事务
COMMIT;

-- ===================================================================
-- 执行说明:
--
-- 1. 备份数据库（重要！）
--    mysqldump -u root -p yph > backup_before_migration_$(date +%Y%m%d).sql
--
-- 2. 执行迁移（Docker 环境）
--    docker-compose exec -T mysql mysql -u yph -pyph123456 yph < sql/migrations/20260727_modify_product_images.sql
--
-- 3. 或者（本地环境）
--    mysql -u root -p yph < sql/migrations/20260727_modify_product_images.sql
--
-- 4. 验证迁移结果
--    docker-compose exec mysql mysql -u yph -pyph123456 yph -e "DESC product;"
--    docker-compose exec mysql mysql -u yph -pyph123456 yph -e "SELECT id, name, main_images, detail_images FROM product LIMIT 5;"
--
-- 5. 重启后端服务
--    docker-compose restart backend
--
-- ===================================================================

-- 验证查询
-- 查看表结构
-- DESCRIBE `product`;

-- 查看迁移后的数据示例
-- SELECT id, name, main_images, detail_images FROM `product` LIMIT 5;
