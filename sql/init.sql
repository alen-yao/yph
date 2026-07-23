-- YPH 电商系统数据库初始化脚本
-- 使用此 SQL 文件初始化数据库，不再使用 Django migrations

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 如果需要重置，先删除所有表
-- DROP TABLE IF EXISTS user, user_role, user_level, delivery_address, user_message, user_points_history, user_login_history;
-- DROP TABLE IF EXISTS product, product_brand, product_category, product_spec, product_spec_value, product_item, product_comment, product_tag;
-- DROP TABLE IF EXISTS `order`, order_item, order_logistics, order_return, cart;
-- DROP TABLE IF EXISTS activity_base, coupon, user_coupon;
-- DROP TABLE IF EXISTS payment_transaction, refund_transaction;
-- DROP TABLE IF EXISTS shop, shop_setting;
-- DROP TABLE IF EXISTS banner, system_config;

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

SET FOREIGN_KEY_CHECKS = 1;

-- 插入默认数据
INSERT INTO `user_level` (`level_name`, `level_discount`, `min_points`, `max_points`, `is_default`, `sort_order`)
VALUES ('普通会员', 1.00, 0, 999, 1, 1) ON DUPLICATE KEY UPDATE `id`=`id`;

INSERT INTO `user_role` (`name`, `description`, `permissions`)
VALUES ('管理员', '系统管理员', '{}') ON DUPLICATE KEY UPDATE `id`=`id`;
