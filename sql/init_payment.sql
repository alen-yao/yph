-- ============================================
-- 支付模块表结构
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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

SET FOREIGN_KEY_CHECKS = 1;
