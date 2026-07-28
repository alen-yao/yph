-- ============================================
-- 交易模块表结构
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 购物车表
CREATE TABLE IF NOT EXISTS `cart` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `product_id` int(11) NOT NULL COMMENT '商品ID',
  `product_item_id` int(11) NOT NULL COMMENT '商品SKU ID',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
  `product_image` varchar(500) DEFAULT '' COMMENT '商品图片',
  `price` decimal(10,2) NOT NULL COMMENT '商品价格',
  `quantity` int(11) NOT NULL DEFAULT 1 COMMENT '数量',
  `is_checked` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否选中',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  CONSTRAINT `fk_cart_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车';

-- 订单表
CREATE TABLE IF NOT EXISTS `order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) NOT NULL UNIQUE COMMENT '订单号',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',

  -- 金额
  `order_amount` decimal(10,2) NOT NULL COMMENT '商品总金额',
  `freight_amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '运费',
  `discount_amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '优惠金额',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',

  -- 状态
  `status` smallint(6) NOT NULL DEFAULT 0 COMMENT '订单状态(0:待支付 1:待发货 2:待收货 3:已完成 4:已取消 5:退款中 6:已退款)',
  `pay_type` smallint(6) DEFAULT NULL COMMENT '支付方式(1:微信 2:支付宝 3:余额 4:货到付款)',

  -- 收货信息
  `consignee` varchar(50) NOT NULL COMMENT '收货人',
  `mobile` varchar(11) NOT NULL COMMENT '手机号',
  `province` varchar(50) NOT NULL COMMENT '省',
  `city` varchar(50) NOT NULL COMMENT '市',
  `district` varchar(50) NOT NULL COMMENT '区/县',
  `address` varchar(200) NOT NULL COMMENT '详细地址',

  -- 备注
  `user_remark` text COMMENT '买家备注',
  `admin_remark` text COMMENT '管理员备注',

  -- 时间
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `ship_time` datetime DEFAULT NULL COMMENT '发货时间',
  `finish_time` datetime DEFAULT NULL COMMENT '完成时间',
  `cancel_time` datetime DEFAULT NULL COMMENT '取消时间',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_time` (`created_time`),
  CONSTRAINT `fk_order_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单';

-- 订单商品表
CREATE TABLE IF NOT EXISTS `order_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `product_id` int(11) NOT NULL COMMENT '商品ID',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
  `product_image` varchar(500) NOT NULL COMMENT '商品图片',
  `product_item_id` int(11) NOT NULL COMMENT 'SKU ID',
  `sku_name` varchar(200) NOT NULL COMMENT 'SKU名称',
  `price` decimal(10,2) NOT NULL COMMENT '商品价格',
  `quantity` int(11) NOT NULL COMMENT '数量',
  `total_amount` decimal(10,2) NOT NULL COMMENT '小计',

  -- 售后
  `is_comment` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否已评价',
  `is_return` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否退货',

  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_product_id` (`product_id`),
  CONSTRAINT `fk_order_item_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单商品';

-- 订单物流表
CREATE TABLE IF NOT EXISTS `order_logistics` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `express_company` varchar(50) DEFAULT '' COMMENT '物流公司',
  `express_no` varchar(50) DEFAULT '' COMMENT '物流单号',
  `express_time` datetime DEFAULT NULL COMMENT '发货时间',
  `logistics_info` text COMMENT '物流信息(JSON)',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_id` (`order_id`),
  CONSTRAINT `fk_order_logistics_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单物流';

-- 退货退款表
CREATE TABLE IF NOT EXISTS `order_return` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `return_no` varchar(50) NOT NULL UNIQUE COMMENT '退款单号',
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `order_item_id` bigint(20) NOT NULL COMMENT '订单商品ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',

  `return_type` smallint(6) NOT NULL COMMENT '退款类型(1:仅退款 2:退货退款)',
  `return_amount` decimal(10,2) NOT NULL COMMENT '退款金额',
  `return_reason` varchar(200) NOT NULL COMMENT '退款原因',
  `return_description` text COMMENT '退款说明',
  `return_images` text COMMENT '凭证图片(JSON)',

  `status` smallint(6) NOT NULL DEFAULT 0 COMMENT '状态(0:待审核 1:审核通过 2:审核拒绝 3:退货中 4:已完成)',
  `admin_remark` text COMMENT '管理员备注',

  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_return_no` (`return_no`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_order_return_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_return_order_item` FOREIGN KEY (`order_item_id`) REFERENCES `order_item` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_return_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='退货退款';

-- 退货原因表
CREATE TABLE IF NOT EXISTS `order_return_reason` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `reason` varchar(100) NOT NULL COMMENT '退货原因',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  `is_enable` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='退货原因';

SET FOREIGN_KEY_CHECKS = 1;

-- 插入示例数据

-- 插入默认退货原因
INSERT INTO `order_return_reason` (`reason`, `sort_order`)
VALUES
  ('不想要了', 1),
  ('商品质量问题', 2),
  ('商品与描述不符', 3),
  ('收到商品破损', 4),
  ('发错货', 5),
  ('其他', 99)
ON DUPLICATE KEY UPDATE `id`=`id`;
