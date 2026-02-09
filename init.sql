-- ================================
-- Check-in System Database Init
-- MySQL 8.x
-- ================================

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS checkin
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE checkin;

-- ================================
-- 2. 用户表
-- ================================
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',

    UNIQUE KEY uniq_username (username)
) ENGINE=InnoDB COMMENT='用户表';

-- ================================
-- 3. 打卡表
-- ================================
DROP TABLE IF EXISTS checkins;

CREATE TABLE checkins (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    checkin_time DATETIME(3) NOT NULL COMMENT '打卡时间（毫秒）',
    checkin_date DATE NOT NULL COMMENT '打卡日期',

    UNIQUE KEY uniq_user_day (user_id, checkin_date),
    KEY idx_day_time (checkin_date, checkin_time),

    CONSTRAINT fk_checkins_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='打卡记录表';

-- ================================
-- 4. 可选：测试用索引验证
-- ================================
-- SELECT NOW(3);
-- INSERT INTO users(username, password_hash) VALUES ('test','x');
-- INSERT INTO checkins(user_id, checkin_date, checkin_time)
-- VALUES (1, CURDATE(), NOW(3));

-- ================================
-- Init Finished
-- ================================
