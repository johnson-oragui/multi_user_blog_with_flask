-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS multi_user_blog;
CREATE USER IF NOT EXISTS 'blog'@'localhost' IDENTIFIED BY 'multi';
GRANT ALL PRIVILEGES ON `multi_user_blog`.* TO 'blog'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'blog'@'localhost';
FLUSH PRIVILEGES;