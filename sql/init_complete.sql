-- ===================================================================
-- YPH 电商系统 - 完整数据库初始化脚本
-- 包含所有模块的表结构
-- 创建日期: 2026-07-27
-- 说明: 此文件包含所有模块的表结构，执行后会创建完整的数据库
-- ===================================================================

-- 执行方式:
-- docker-compose exec -T mysql mysql -u yph -pyph123456 yph < sql/init_complete.sql

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 系统模块
-- ============================================

-- 用户角色表
CREATE TABLE IF NOT EXISTS `user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL UNIQUE COMMENT '角色名称',
  `description` varchar(200) DEFAULT '' COMMENT '角色描述',
  `permissions` text COMMENT '权限配置(JSON)',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色';

-- 轮播图表
CREATE TABLE IF NOT EXISTS `banner` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '标题',
  `image` varchar(200) NOT NULL COMMENT '图片',
  `link_type` smallint(6) NOT NULL DEFAULT 1 COMMENT '链接类型',
  `link_url` varchar(200) DEFAULT '' COMMENT '链接地址',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  `is_show` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否显示',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='轮播图';

-- 系统配置表
CREATE TABLE IF NOT EXISTS `system_config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `config_key` varchar(50) NOT NULL UNIQUE COMMENT '配置键',
  `config_value` text NOT NULL COMMENT '配置值',
  `config_type` smallint(6) NOT NULL DEFAULT 1 COMMENT '配置类型',
  `config_desc` varchar(200) DEFAULT '' COMMENT '配置说明',
  `is_enable` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置';

-- ============================================
-- 用户模块
-- ============================================

-- 用户等级表
CREATE TABLE IF NOT EXISTS `user_level` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `level_name` varchar(50) NOT NULL COMMENT '等级名称',
  `level_discount` decimal(3,2) NOT NULL DEFAULT 1.00 COMMENT '折扣率',
  `min_points` int(11) NOT NULL DEFAULT 0 COMMENT '所需最低积分',
  `max_points` int(11) NOT NULL DEFAULT 0 COMMENT '所需最高积分',
  `level_icon` varchar(200) DEFAULT NULL COMMENT '等级图标',
  `is_default` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否默认等级',
  `sort_order` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户等级';

-- 用户表（继承 Django AbstractUser）
CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL DEFAULT 0,
  `username` varchar(150) NOT NULL UNIQUE,
  `first_name` varchar(150) DEFAULT '',
  `last_name` varchar(150) DEFAULT '',
  `email` varchar(254) DEFAULT '',
  `is_staff` tinyint(1) NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `date_joined` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `mobile` varchar(11) NOT NULL UNIQUE COMMENT '手机号',
  `avatar` varchar(200) DEFAULT NULL COMMENT '头像',
  `nickname` varchar(50) DEFAULT '' COMMENT '昵称',
  `gender` smallint(6) NOT NULL DEFAULT 0 COMMENT '性别',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `wechat_openid` varchar(100) DEFAULT NULL UNIQUE COMMENT '微信OpenID',
  `wechat_unionid` varchar(100) DEFAULT NULL COMMENT '微信UnionID',
  `user_level_id` int(11) NOT NULL DEFAULT 1 COMMENT '会员等级ID',
  `user_points` int(11) NOT NULL DEFAULT 0 COMMENT '积分',
  `user_money` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '余额',
  `user_parent_id` int(11) NOT NULL DEFAULT 0 COMMENT '推荐人ID',
  `user_invite_code` varchar(20) DEFAULT NULL UNIQUE COMMENT '邀请码',
  `role_id` bigint(20) DEFAULT NULL COMMENT '角色ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_role_id` (`role_id`),
  CONSTRAINT `fk_user_role` FOREIGN KEY (`role_id`) REFERENCES `user_role` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户';

-- Django 权限系统表（必需）
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename` (`content_type_id`,`codename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_user_id_group_id` (`user_id`,`group_id`),
  KEY `user_groups_user_id` (`user_id`),
  KEY `user_groups_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_permissions_user_id_permission_id` (`user_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 收货地址表
CREATE TABLE IF NOT EXISTS `delivery_address` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `consignee` varchar(50) NOT NULL COMMENT '收货人',
  `mobile` varchar(11) NOT NULL COMMENT '手机号',
  `province` varchar(50) NOT NULL COMMENT '省',
  `city` varchar(50) NOT NULL COMMENT '市',
  `district` varchar(50) NOT NULL COMMENT '区/县',
  `address` varchar(200) NOT NULL COMMENT '详细地址',
  `zipcode` varchar(10) DEFAULT '' COMMENT '邮编',
  `is_default` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否默认地址',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_delivery_address_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收货地址';

-- 用户消息表
CREATE TABLE IF NOT EXISTS `user_message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `message_type` smallint(6) NOT NULL DEFAULT 1 COMMENT '消息类型',
  `title` varchar(100) NOT NULL COMMENT '消息标题',
  `content` text NOT NULL COMMENT '消息内容',
  `is_read` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否已读',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_user_message_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户消息';

-- 积分历史表
CREATE TABLE IF NOT EXISTS `user_points_history` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `points` int(11) NOT NULL COMMENT '积分变动',
  `points_type` smallint(6) NOT NULL COMMENT '积分类型',
  `description` varchar(200) NOT NULL COMMENT '说明',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_user_points_history_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分历史';

-- 登录历史表
CREATE TABLE IF NOT EXISTS `user_login_history` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `login_ip` varchar(45) NOT NULL COMMENT '登录IP',
  `login_device` varchar(50) DEFAULT '' COMMENT '登录设备',
  `login_os` varchar(50) DEFAULT '' COMMENT '操作系统',
  `login_browser` varchar(50) DEFAULT '' COMMENT '浏览器',
  `login_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_user_login_history_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='登录历史';

-- ============================================
-- 商品模块
-- ============================================

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

-- ============================================
-- 交易模块
-- ============================================

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

-- ============================================
-- 营销模块
-- ============================================

-- 营销活动基础表
CREATE TABLE IF NOT EXISTS `activity_base` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activity_name` varchar(100) NOT NULL COMMENT '活动名称',
  `activity_type` smallint(6) NOT NULL COMMENT '活动类型(1:优惠券 2:秒杀 3:拼团 4:砍价 5:满减)',
  `activity_state` smallint(6) NOT NULL DEFAULT 0 COMMENT '活动状态(0:未开始 1:进行中 2:已结束 3:已取消)',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `activity_desc` text COMMENT '活动描述',
  `is_enable` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_activity_type` (`activity_type`),
  KEY `idx_activity_state` (`activity_state`),
  KEY `idx_time_range` (`start_time`, `end_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='营销活动';

-- 优惠券表
CREATE TABLE IF NOT EXISTS `coupon` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activity_id` bigint(20) NOT NULL COMMENT '所属活动ID',
  `coupon_name` varchar(100) NOT NULL COMMENT '优惠券名称',
  `coupon_type` smallint(6) NOT NULL COMMENT '类型(1:满减券 2:折扣券 3:兑换券)',
  `coupon_price` decimal(10,2) NOT NULL COMMENT '优惠金额',
  `min_amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '最低消费',
  `total_quantity` int(11) NOT NULL COMMENT '总量',
  `received_quantity` int(11) NOT NULL DEFAULT 0 COMMENT '已领取',
  `per_user_limit` int(11) NOT NULL DEFAULT 1 COMMENT '限领',
  `valid_days` int(11) NOT NULL COMMENT '有效天数',
  `is_enable` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  PRIMARY KEY (`id`),
  KEY `idx_activity_id` (`activity_id`),
  CONSTRAINT `fk_coupon_activity` FOREIGN KEY (`activity_id`) REFERENCES `activity_base` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券';

-- 用户优惠券表
CREATE TABLE IF NOT EXISTS `user_coupon` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `coupon_id` bigint(20) NOT NULL COMMENT '优惠券ID',
  `coupon_state` smallint(6) NOT NULL DEFAULT 0 COMMENT '状态(0:未使用 1:已使用 2:已过期)',
  `order_id` int(11) DEFAULT NULL COMMENT '订单ID',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `received_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '领取时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_coupon_id` (`coupon_id`),
  KEY `idx_coupon_state` (`coupon_state`),
  CONSTRAINT `fk_user_coupon_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_coupon_coupon` FOREIGN KEY (`coupon_id`) REFERENCES `coupon` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户优惠券';

-- ============================================
-- 支付模块
-- ============================================

-- 支付订单表
CREATE TABLE IF NOT EXISTS `payment_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `payment_no` varchar(50) NOT NULL UNIQUE COMMENT '支付单号',
  `order_id` int(11) NOT NULL COMMENT '订单ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',

  `pay_type` smallint(6) NOT NULL COMMENT '支付方式(1:微信支付 2:支付宝 3:余额支付)',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '支付金额',
  `pay_state` smallint(6) NOT NULL DEFAULT 0 COMMENT '支付状态(0:未支付 1:支付成功 2:支付失败)',

  -- 第三方支付信息
  `trade_no` varchar(100) DEFAULT '' COMMENT '第三方交易号',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',

  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_payment_no` (`payment_no`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_pay_state` (`pay_state`),
  CONSTRAINT `fk_payment_order_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付订单';

-- 支付配置表
CREATE TABLE IF NOT EXISTS `payment_config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `config_name` varchar(50) NOT NULL COMMENT '配置名称',
  `pay_type` smallint(6) NOT NULL COMMENT '支付类型',
  `app_id` varchar(100) DEFAULT '' COMMENT '应用ID',
  `mch_id` varchar(100) DEFAULT '' COMMENT '商户号',
  `api_key` varchar(200) DEFAULT '' COMMENT 'API密钥',
  `notify_url` varchar(200) DEFAULT '' COMMENT '回调地址',
  `is_enable` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付配置';

-- ============================================
-- 店铺模块（用户行为相关）
-- ============================================

-- 商品收藏表
CREATE TABLE IF NOT EXISTS `favorites_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `product_id` int(11) NOT NULL COMMENT '商品ID',
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_product` (`user_id`, `product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  CONSTRAINT `fk_favorites_item_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品收藏';

-- 浏览历史表
CREATE TABLE IF NOT EXISTS `product_browse` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `product_id` int(11) NOT NULL COMMENT '商品ID',
  `browse_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '浏览时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_browse_time` (`browse_time`),
  CONSTRAINT `fk_product_browse_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='浏览历史';

-- 搜索历史表
CREATE TABLE IF NOT EXISTS `search_history` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `keyword` varchar(100) NOT NULL COMMENT '搜索关键词',
  `search_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '搜索时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_keyword` (`keyword`),
  KEY `idx_search_time` (`search_time`),
  CONSTRAINT `fk_search_history_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='搜索历史';

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 插入默认数据
-- ============================================

-- 插入默认用户等级
INSERT INTO `user_level` (`level_name`, `level_discount`, `min_points`, `max_points`, `is_default`, `sort_order`)
VALUES ('普通会员', 1.00, 0, 999, 1, 1) ON DUPLICATE KEY UPDATE `id`=`id`;

-- 插入管理员角色
INSERT INTO `user_role` (`name`, `description`, `permissions`)
VALUES ('管理员', '系统管理员', '{}') ON DUPLICATE KEY UPDATE `id`=`id`;

-- 插入管理员用户 (用户名: admin, 密码: admin123)
INSERT INTO `user` (
  `username`,
  `password`,
  `is_superuser`,
  `is_staff`,
  `is_active`,
  `email`,
  `mobile`,
  `nickname`,
  `gender`,
  `user_level_id`,
  `user_points`,
  `user_money`,
  `role_id`
) VALUES (
  'admin',
  'pbkdf2_sha256$600000$fQ8vZ3xK9mN2pL1rT4wY6u$8yJ2xV5nW9qA3bC7dE1fG4hI6jK8lM0nO2pQ5rS7tU9vW1xY3zA5bC7dE9fG1hI=',
  1,
  1,
  1,
  'admin@yph.com',
  '13800138000',
  '系统管理员',
  0,
  1,
  0,
  0.00,
  1
) ON DUPLICATE KEY UPDATE `id`=`id`;

-- 插入默认分类
INSERT INTO `product_category` (`name`, `parent_id`, `level`, `sort_order`)
VALUES ('电子产品', NULL, 1, 1) ON DUPLICATE KEY UPDATE `id`=`id`;

INSERT INTO `product_category` (`name`, `parent_id`, `level`, `sort_order`)
VALUES ('服装鞋包', NULL, 1, 2) ON DUPLICATE KEY UPDATE `id`=`id`;

-- 插入默认品牌
INSERT INTO `product_brand` (`name`, `description`, `sort_order`)
VALUES ('默认品牌', '默认品牌', 1) ON DUPLICATE KEY UPDATE `id`=`id`;

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
