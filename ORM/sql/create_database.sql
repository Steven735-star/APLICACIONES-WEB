CREATE DATABASE IF NOT EXISTS orm_workshop
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'ormuser'@'localhost'
IDENTIFIED BY 'ormpass123';

GRANT ALL PRIVILEGES
ON orm_workshop.*
TO 'ormuser'@'localhost';

FLUSH PRIVILEGES;
