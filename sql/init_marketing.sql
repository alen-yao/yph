-- ============================================
-- 营销模块表结构
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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

SET FOREIGN_KEY_CHECKS = 1;
