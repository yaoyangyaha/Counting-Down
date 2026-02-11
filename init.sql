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

    points INT NOT NULL DEFAULT 0 COMMENT '年度积分',

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
-- 4. 系统配置表（用于年度积分重置）
-- ================================
DROP TABLE IF EXISTS system_config;

CREATE TABLE system_config (
    config_key VARCHAR(50) PRIMARY KEY,
    config_value VARCHAR(100) NOT NULL
) ENGINE=InnoDB COMMENT='系统配置表';

-- 初始化当前积分年度
INSERT INTO system_config (config_key, config_value)
VALUES ('points_year', '2026');
