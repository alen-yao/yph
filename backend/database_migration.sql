-- ============================================
-- 地区和分类改造SQL脚本
-- 执行顺序：从上到下依次执行
-- ============================================

-- 1. 创建 region 表
CREATE TABLE IF NOT EXISTS `region` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `code` varchar(20) NOT NULL UNIQUE COMMENT '地区代码',
    `name` varchar(50) NOT NULL COMMENT '地区名称',
    `icon` varchar(100) NOT NULL DEFAULT '' COMMENT '图标路径',
    `sort_order` int NOT NULL DEFAULT 0 COMMENT '排序',
    `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否启用',
    `created_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    `updated_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_status` (`status`),
    KEY `idx_sort_order` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地区表';

-- 2. 初始化34个省份数据
INSERT INTO `region` (`code`, `name`, `icon`, `sort_order`, `status`) VALUES
('110000', '北京市', '110000.png', 1, 0),
('120000', '天津市', '120000.png', 2, 0),
('130000', '河北省', '130000.png', 3, 0),
('140000', '山西省', '140000.png', 4, 0),
('150000', '内蒙古自治区', '150000.png', 5, 0),
('210000', '辽宁省', '210000.png', 6, 0),
('220000', '吉林省', '220000.png', 7, 0),
('230000', '黑龙江省', '230000.png', 8, 0),
('310000', '上海市', '310000.png', 9, 0),
('320000', '江苏省', '320000.png', 10, 0),
('330000', '浙江省', '330000.png', 11, 0),
('340000', '安徽省', '340000.png', 12, 0),
('350000', '福建省', '350000.png', 13, 0),
('360000', '江西省', '360000.png', 14, 0),
('370000', '山东省', '370000.png', 15, 0),
('410000', '河南省', '410000.png', 16, 0),
('420000', '湖北省', '420000.png', 17, 0),
('430000', '湖南省', '430000.png', 18, 0),
('440000', '广东省', '440000.png', 19, 0),
('450000', '广西壮族自治区', '450000.png', 20, 0),
('460000', '海南省', '460000.png', 21, 0),
('500000', '重庆市', '500000.png', 22, 0),
('510000', '四川省', '510000.png', 23, 0),
('520000', '贵州省', '520000.png', 24, 0),
('530000', '云南省', '530000.png', 25, 0),
('540000', '西藏自治区', '540000.png', 26, 0),
('610000', '陕西省', '610000.png', 27, 0),
('620000', '甘肃省', '620000.png', 28, 0),
('630000', '青海省', '630000.png', 29, 0),
('640000', '宁夏回族自治区', '640000.png', 30, 0),
('650000', '新疆维吾尔自治区', '650000.png', 31, 0),
('710000', '台湾省', '710000.png', 32, 0),
('810000', '香港特别行政区', '810000.png', 33, 0),
('820000', '澳门特别行政区', '820000.png', 34, 0);

-- 3. 修改 product_category 表（删除 parent_id 和 level 字段）
-- 注意：如果你的分类表已有数据且有二级分类，请先备份数据！

-- 检查是否存在这些字段，如果存在则删除
SET @db_name = DATABASE();

-- 删除 parent_id 字段
SET @col_exists = (SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @db_name
    AND TABLE_NAME = 'product_category'
    AND COLUMN_NAME = 'parent_id');

SET @sql = IF(@col_exists > 0,
    'ALTER TABLE `product_category` DROP FOREIGN KEY `product_category_parent_id_fk`;',
    'SELECT "parent_id foreign key does not exist" AS message;');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = IF(@col_exists > 0,
    'ALTER TABLE `product_category` DROP COLUMN `parent_id`;',
    'SELECT "parent_id column does not exist" AS message;');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 删除 level 字段
SET @col_exists = (SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @db_name
    AND TABLE_NAME = 'product_category'
    AND COLUMN_NAME = 'level');

SET @sql = IF(@col_exists > 0,
    'ALTER TABLE `product_category` DROP COLUMN `level`;',
    'SELECT "level column does not exist" AS message;');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 4. 修改 product 表（添加 region_id 字段）
-- 先检查字段是否已存在
SET @col_exists = (SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @db_name
    AND TABLE_NAME = 'product'
    AND COLUMN_NAME = 'region_id');

-- 如果不存在则添加
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE `product` ADD COLUMN `region_id` bigint NULL COMMENT ''所属地区'' AFTER `id`;',
    'SELECT "region_id column already exists" AS message;');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加外键约束（如果字段是新添加的）
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE `product` ADD CONSTRAINT `product_region_id_fk` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`) ON DELETE CASCADE;',
    'SELECT "region_id foreign key may already exist" AS message;');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加索引
SET @idx_exists = (SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE TABLE_SCHEMA = @db_name
    AND TABLE_NAME = 'product'
    AND INDEX_NAME = 'idx_region_id');

SET @sql = IF(@idx_exists = 0,
    'ALTER TABLE `product` ADD INDEX `idx_region_id` (`region_id`);',
    'SELECT "idx_region_id already exists" AS message;');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================
-- 重要提示：
-- 1. 执行完后，需要手动为现有的商品数据设置 region_id
--    示例：UPDATE product SET region_id = 1 WHERE id > 0;
-- 2. 然后将 region_id 字段改为 NOT NULL：
--    ALTER TABLE `product` MODIFY COLUMN `region_id` bigint NOT NULL;
-- 3. 在 Django Admin 中启用需要的地区
-- ============================================

-- 查询执行结果
SELECT 'Migration completed successfully!' AS status;
SELECT COUNT(*) AS region_count FROM region;
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'product'
AND COLUMN_NAME = 'region_id';
