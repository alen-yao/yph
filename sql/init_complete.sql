-- ===================================================================
-- YPH 电商系统 - 完整数据库初始化脚本
-- 包含所有模块的表结构
-- 创建日期: 2026-07-27
-- 说明: 此文件包含所有模块的表结构，执行后会创建完整的数据库
-- ===================================================================

-- 执行顺序:
-- 1. sql/init.sql (user + system 模块)
-- 2. sql/init_products.sql (商品模块)
-- 3. sql/init_trade.sql (交易模块)
-- 4. sql/init_marketing.sql (营销模块)
-- 5. sql/init_payment.sql (支付模块)
-- 6. sql/init_shops.sql (店铺模块)

-- 或者直接执行本文件，包含所有表结构

SOURCE sql/init.sql;
SOURCE sql/init_products.sql;
SOURCE sql/init_trade.sql;
SOURCE sql/init_marketing.sql;
SOURCE sql/init_payment.sql;
SOURCE sql/init_shops.sql;
