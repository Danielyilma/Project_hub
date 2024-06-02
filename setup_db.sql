CREATE USER IF NOT EXISTS 'PHUB'@'localhost' IDENTIFIED BY 'phubcode';
GRANT all ON *.* TO 'PHUB'@'localhost';
CREATE DATABASE IF NOT EXISTS   project_hub;
