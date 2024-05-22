-- Script prepares MySQL server
-- DATABASE cuisine_dev_db
-- User cuisine_dev (in localhost)

CREATE DATABASE IF NOT EXISTS cuisine_dev_db;

CREATE USER
IF NOT EXISTS 'cuisine_dev'@'localhost'
	IDENTIFIED BY 'Cuisine_dev_pwd2024**';

GRANT ALL PRIVILEGES ON cuisine_dev_db.*
TO 'cuisine_dev'@'localhost';
