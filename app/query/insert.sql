CREATE DATABASE IF NOT EXISTS test;

USE test;

SET NAMES utf8;
SET time_zone = '+70:00';
SET foreign_key_checks = 0;
SET sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Creating table SYS_USER
DROP TABLE IF EXISTS `SYS_USER`;
CREATE TABLE `SYS_USER` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(255) UNIQUE NOT NULL,
    `hash_password` VARCHAR(255),
    `phone` VARCHAR(20),
    `email` VARCHAR(255),
    `full_name` VARCHAR(255),
    `status` NUMERIC,
    `created_at` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `created_by` INT, -- id user who created new user
    `updated_by` INT  -- id user who updated user
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Creating table SYS_ROLE
DROP TABLE IF EXISTS `SYS_ROLE`;
CREATE TABLE `SYS_ROLE` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255),
    `description` VARCHAR(255),
    `status` NUMERIC,
    `created_at` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `created_by` INT, -- id user who created new user
    `updated_by` INT  -- id user who updated user
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Creating table SYS_USER_ROLE
DROP TABLE IF EXISTS `SYS_USER_ROLE`;
CREATE TABLE `SYS_USER_ROLE` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT REFERENCES SYS_USER(id),
    `role_id` INT REFERENCES SYS_ROLE(id),
    `created_at` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    `created_by` INT -- id user who created new user role
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Creating table SYS_FUNCTION
DROP TABLE IF EXISTS `SYS_FUNCTION`;
CREATE TABLE `SYS_FUNCTION` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255),
    `path` VARCHAR(255),
    `description` VARCHAR(255),
    `parent_id` INT REFERENCES SYS_FUNCTION(id),
    `type` VARCHAR(50),
    `status` NUMERIC, -- 0 - ok, 1 - stop
    `icon_url` VARCHAR(255),
    `created_at` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `created_by` INT, -- id user who created new SYS_FUNCTION
    `updated_by` INT  -- id user who updated SYS_FUNCTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Creating table SYS_ROLE_FUNCTION
DROP TABLE IF EXISTS `SYS_ROLE_FUNCTION`;
CREATE TABLE `SYS_ROLE_FUNCTION` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `role_id` INT REFERENCES SYS_ROLE(id),
    `function_id` INT REFERENCES SYS_FUNCTION(id),
    `created_at` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    `created_by` INT -- id user who created new SYS_ROLE_FUNCTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Creating table SYS_LOG
DROP TABLE IF EXISTS `SYS_LOG`;
CREATE TABLE SYS_LOG (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `action_datetime` TIMESTAMP,
    `path_name` VARCHAR(255),
    `method` VARCHAR(50),
    `ip` VARCHAR(50),
    `status_response` VARCHAR(50), -- http status res
    `response` VARCHAR(255),  -- msg res
    `description` VARCHAR(255),
    `request` VARCHAR(255),   -- body query
    `duration` FLOAT -- time from req to res
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Creating table DATA_DICTIONARY
DROP TABLE IF EXISTS `DATA_DICTIONARY`;
CREATE TABLE `DATA_DICTIONARY` (
    `id` int PRIMARY KEY AUTO_INCREMENT,
    `table_name` VARCHAR(255),
    `column_name` VARCHAR(255),
    `description` VARCHAR(255),
    `value` INT  -- enum for each column name
)ENGINE=InnoDB DEFAULT CHARSET=utf8;