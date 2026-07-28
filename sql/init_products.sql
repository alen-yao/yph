-- ============================================
-- 商品模块表结构
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 商品分类表
CREATE TABLE IF NOT EXISTS `product_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `parent_id` bigint(20) DEFAULT NULL COMMENT '父分类ID',
  `level` smallint(6) NOT NULL DEFAULT 1 COMMENT '分类层级',
  `icon` varchar(200) DEFAULT NULL COMMENT '分类图标',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  `is_show` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否显示',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  CONSTRAINT `fk_product_category_parent` FOREIGN KEY (`parent_id`) REFERENCES `product_category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类';

-- 商品品牌表
CREATE TABLE IF NOT EXISTS `product_brand` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '品牌名称',
  `logo` varchar(200) DEFAULT NULL COMMENT '品牌Logo',
  `description` text COMMENT '品牌描述',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  `is_show` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否显示',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品品牌';

-- 商品表（支持 MinIO 多图）
CREATE TABLE IF NOT EXISTS `product` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL COMMENT '商品名称',
  `category_id` bigint(20) NOT NULL COMMENT '商品分类ID',
  `brand_id` bigint(20) DEFAULT NULL COMMENT '品牌ID',

  -- MinIO 图片存储
  `main_images` JSON DEFAULT NULL COMMENT '主图列表(JSON数组)，第一张为封面图',
  `detail_images` JSON DEFAULT NULL COMMENT '详情图列表(JSON数组)，按顺序展示',

  -- 商品详情
  `description` text COMMENT '商品简介',
  `detail_html` text COMMENT '商品详情HTML',

  -- 价格和库存
  `price` decimal(10,2) NOT NULL COMMENT '销售价格',
  `market_price` decimal(10,2) NOT NULL COMMENT '市场价格',
  `cost_price` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '成本价',
  `stock` int(11) NOT NULL DEFAULT 0 COMMENT '总库存',

  -- 销量和评分
  `sales_count` int(11) NOT NULL DEFAULT 0 COMMENT '销量',
  `view_count` int(11) NOT NULL DEFAULT 0 COMMENT '浏览量',
  `favorite_count` int(11) NOT NULL DEFAULT 0 COMMENT '收藏量',
  `comment_count` int(11) NOT NULL DEFAULT 0 COMMENT '评论数',
  `rating_average` decimal(3,2) NOT NULL DEFAULT 5.00 COMMENT '平均评分',

  -- 状态
  `state` smallint(6) NOT NULL DEFAULT 1 COMMENT '商品状态(0:下架 1:上架)',
  `is_recommend` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否推荐',
  `is_new` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否新品',
  `is_hot` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否热销',

  -- 排序和时间
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_brand_id` (`brand_id`),
  KEY `idx_state` (`state`),
  CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_brand` FOREIGN KEY (`brand_id`) REFERENCES `product_brand` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品';

-- 商品规格表
CREATE TABLE IF NOT EXISTS `product_spec` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '规格名称',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品规格';

-- 商品规格值表
CREATE TABLE IF NOT EXISTS `product_spec_value` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `spec_id` bigint(20) NOT NULL COMMENT '所属规格ID',
  `value` varchar(50) NOT NULL COMMENT '规格值',
  `image` varchar(200) DEFAULT NULL COMMENT '规格图片',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  PRIMARY KEY (`id`),
  KEY `idx_spec_id` (`spec_id`),
  CONSTRAINT `fk_product_spec_value_spec` FOREIGN KEY (`spec_id`) REFERENCES `product_spec` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品规格值';

-- 商品SKU表
CREATE TABLE IF NOT EXISTS `product_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
  `sku_code` varchar(50) NOT NULL UNIQUE COMMENT 'SKU编码',
  `spec_values` text NOT NULL COMMENT '规格值(JSON)',
  `image` varchar(200) DEFAULT NULL COMMENT 'SKU图片',
  `price` decimal(10,2) NOT NULL COMMENT '价格',
  `cost_price` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '成本价',
  `stock` int(11) NOT NULL DEFAULT 0 COMMENT '库存',
  `sales_count` int(11) NOT NULL DEFAULT 0 COMMENT '销量',
  `is_enable` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_sku_code` (`sku_code`),
  CONSTRAINT `fk_product_item_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品SKU';

-- 商品评论表
CREATE TABLE IF NOT EXISTS `product_comment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `order_id` int(11) NOT NULL COMMENT '订单ID',
  `content` text NOT NULL COMMENT '评论内容',
  `images` text COMMENT '评论图片(JSON)',
  `rating` smallint(6) NOT NULL DEFAULT 5 COMMENT '评分(1-5)',
  `comment_level` smallint(6) NOT NULL DEFAULT 3 COMMENT '评价等级(1:差评 2:中评 3:好评)',
  `reply_content` text COMMENT '商家回复',
  `reply_time` datetime DEFAULT NULL COMMENT '回复时间',
  `helpful_count` int(11) NOT NULL DEFAULT 0 COMMENT '有用数',
  `is_show` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否显示',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '评论时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_product_comment_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评论';

-- 商品标签表
CREATE TABLE IF NOT EXISTS `product_tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '标签名称',
  `color` varchar(20) NOT NULL DEFAULT '#FF0000' COMMENT '标签颜色',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品标签';

SET FOREIGN_KEY_CHECKS = 1;

-- 插入示例数据

-- 插入默认分类
INSERT INTO `product_category` (`name`, `parent_id`, `level`, `sort_order`)
VALUES ('电子产品', NULL, 1, 1) ON DUPLICATE KEY UPDATE `id`=`id`;

INSERT INTO `product_category` (`name`, `parent_id`, `level`, `sort_order`)
VALUES ('服装鞋包', NULL, 1, 2) ON DUPLICATE KEY UPDATE `id`=`id`;

-- 插入默认品牌
INSERT INTO `product_brand` (`name`, `description`, `sort_order`)
VALUES ('默认品牌', '默认品牌', 1) ON DUPLICATE KEY UPDATE `id`=`id`;
