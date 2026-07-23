-- 数据库变更模板
-- 日期: YYYY-MM-DD
-- 作者: YourName
-- 说明: 这里描述此次变更的目的

-- 复制此模板，按照 YYYYMMDD_description.sql 格式命名
-- 例如: 20260722_add_user_avatar_field.sql

-- 示例1：添加字段
-- ALTER TABLE `user`
-- ADD COLUMN `avatar_url` VARCHAR(255) DEFAULT NULL COMMENT '头像URL';

-- 示例2：修改字段
-- ALTER TABLE `user`
-- MODIFY COLUMN `nickname` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '用户昵称';

-- 示例3：添加索引
-- ALTER TABLE `user`
-- ADD INDEX `idx_mobile` (`mobile`);

-- 示例4：创建新表
-- CREATE TABLE IF NOT EXISTS `new_table` (
--   `id` bigint(20) NOT NULL AUTO_INCREMENT,
--   `name` varchar(100) NOT NULL COMMENT '名称',
--   `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='新表';

-- 执行此 SQL:
-- docker-compose exec mysql mysql -u yph -pyph123456 -D yph < sql/migrations/filename.sql
