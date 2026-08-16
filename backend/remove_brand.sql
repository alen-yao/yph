-- 删除商品品牌功能的SQL脚本
-- 执行前请备份数据库！

USE yph_db;

-- 临时禁用外键检查
SET FOREIGN_KEY_CHECKS = 0;

-- 1. 删除外键约束
ALTER TABLE product DROP FOREIGN KEY fk_product_brand;

-- 2. 删除 brand_id 字段
ALTER TABLE product DROP COLUMN brand_id;

-- 3. 删除 product_brand 表
DROP TABLE IF EXISTS product_brand;

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- 验证：查看 product 表结构，确认 brand_id 字段已删除
SELECT '=== Product 表结构 ===' AS '';
SHOW COLUMNS FROM product;

-- 验证：确认 product_brand 表已删除
SELECT '=== 检查 product_brand 表是否存在 ===' AS '';
SHOW TABLES LIKE 'product_brand';
