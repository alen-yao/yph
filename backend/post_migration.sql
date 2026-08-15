-- ============================================
-- 迁移后的数据处理脚本
-- 在执行完 database_migration.sql 后执行此脚本
-- ============================================

-- ============================================
-- 第一步：为现有商品设置默认地区
-- ============================================
-- 方案1：如果你的商品数量不多，可以手动在Django Admin中逐个设置

-- 方案2：批量设置为某个默认地区（例如：北京市 id=1）
-- 取消下面的注释来执行
-- UPDATE `product` SET `region_id` = 1 WHERE `region_id` IS NULL;

-- 方案3：如果商品表为空，直接执行下一步即可

-- ============================================
-- 第二步：将 region_id 字段改为必填（NOT NULL）
-- ============================================
-- 确保上面的步骤已执行，所有商品都有 region_id 后再执行

-- 检查是否还有 NULL 值
SELECT COUNT(*) AS products_without_region FROM `product` WHERE `region_id` IS NULL;

-- 如果上面查询结果为 0，则执行以下语句
-- ALTER TABLE `product` MODIFY COLUMN `region_id` bigint NOT NULL COMMENT '所属地区';

-- ============================================
-- 第三步：启用需要的地区
-- ============================================
-- 示例：启用北京、上海、广东、四川
-- UPDATE `region` SET `status` = 1 WHERE `code` IN ('110000', '310000', '440000', '510000');

-- 或者启用所有地区
-- UPDATE `region` SET `status` = 1;

-- ============================================
-- 验证数据
-- ============================================
-- 查看启用的地区列表
SELECT `id`, `code`, `name`, `sort_order`, `status`
FROM `region`
WHERE `status` = 1
ORDER BY `sort_order`;

-- 查看每个地区的商品数量
SELECT
    r.name AS region_name,
    COUNT(p.id) AS product_count
FROM `region` r
LEFT JOIN `product` p ON r.id = p.region_id
GROUP BY r.id, r.name
ORDER BY r.sort_order;

-- 查看分类列表（确认没有 parent_id 和 level 字段）
SELECT * FROM `product_category` LIMIT 5;

-- ============================================
-- 常用维护SQL
-- ============================================

-- 调整地区排序（示例：把四川排到第一位）
-- UPDATE `region` SET `sort_order` = 0 WHERE `code` = '510000';

-- 批量启用某些地区
-- UPDATE `region` SET `status` = 1 WHERE `code` IN ('110000', '310000', '440000');

-- 禁用某个地区
-- UPDATE `region` SET `status` = 0 WHERE `code` = '710000';

-- 查看某个分类下的商品数量
-- SELECT category_id, COUNT(*) AS count
-- FROM `product`
-- GROUP BY category_id;
