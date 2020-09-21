SHOW DATABASES;

DROP DATABASE psyx;

CREATE DATABASE psyx;
USE psyx;
SHOW TABLES;

DROP TABLE IF EXISTS `pack`;
DROP TABLE IF EXISTS `reply`;

CREATE TABLE `pack` (
    `p_id` INT NOT NULL AUTO_INCREMENT,
    `sex` TINYINT NOT NULL,
    `age_min` TINYINT NOT NULL,
    `age_max` TINYINT NOT NULL,
    `pack_name` CHAR(32) NOT NULL UNIQUE, 
    `date` DATETIME NOT NULL,
    PRIMARY KEY (`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `reply` (
    `r_id` INT NOT NULL AUTO_INCREMENT,
    `p_id` INT NOT NULL,
    `name` CHAR(64) NOT NULL,
    `email` CHAR(48) NOT NULL,
    `no` CHAR(16) NOT NULL,
    `sex` TINYINT NOT NULL,
    `age` TINYINT NOT NULL,
    `phone` CHAR(48) NOT NULL,
    `date` DATETIME NOT NULL,
    `answers` JSON NOT NULL,
    PRIMARY KEY (`r_id`),
    FOREIGN KEY (`p_id`) REFERENCES `pack`(`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DESCRIBE pack;
DESCRIBE reply;

SELECT * FROM `pack`;
SELECT * FROM `reply`;
--SELECT p.*, r.count FROM pack p LEFT JOIN (SELECT p_id, COUNT(*) count FROM reply GROUP BY p_id) r ON p.p_id=r.p_id;