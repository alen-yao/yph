-- 删除商品品牌功能的SQL脚本
-- 执行前请备份数据库！

-- 1. 删除 product 表的 brand_id 外键约束
-- 首先查找外键约束名称
SELECT CONSTRAINT_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'yph_db'
  AND TABLE_NAME = 'product'
  AND COLUMN_NAME = 'brand_id';

-- 删除外键约束（请将下面的约束名称替换为上面查询到的实际名称）
-- ALTER TABLE product DROP FOREIGN KEY product_brand_id_xxxx;

-- 通用方法：先禁用外键检查，删除字段，再启用
SET FOREIGN_KEY_CHECKS = 0;

-- 2. 删除 product 表中的 brand_id 字段
ALTER TABLE product DROP COLUMN brand_id;

-- 3. 删除 product_brand 表
DROP TABLE IF EXISTS product_brand;

-- 4. 重新启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- 验证：查看 product 表结构，确认 brand_id 字段已删除
SHOW COLUMNS FROM product;

-- 验证：确认 product_brand 表已删除
SHOW TABLES LIKE 'product_brand';
