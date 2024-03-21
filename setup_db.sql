-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS hms_dev_db;
CREATE USER IF NOT EXISTS 'hms_dev'@'localhost' IDENTIFIED BY 'hms_dev_pwd';
GRANT ALL PRIVILEGES ON `hms_dev_db`.* TO 'hms_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'hms_dev'@'localhost';
FLUSH PRIVILEGES;