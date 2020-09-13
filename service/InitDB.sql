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
    `age_lower` TINYINT NOT NULL,
    `age_upper` TINYINT NOT NULL,
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
    `answer` JSON NOT NULL,
    PRIMARY KEY (`r_id`),
    FOREIGN KEY (`p_id`) REFERENCES `pack`(`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DESCRIBE pack;
DESCRIBE reply;

INSERT INTO `pack` VALUES (NULL, 1, 20, 30, 'animal', sysdate());
INSERT INTO `reply` VALUES (NULL, 1, '일일일', 'aaaa@gmail.com', '111111111', 1, 25, '고려대학교', sysdate(), '[
    ["j", 2.4401],
    [" ", 3.0000],
    ["i", 1.0433],
    ["i", 2.6569],
    ["j", 2.1122]
]');
INSERT INTO `reply` VALUES (NULL, 10, '이이이', 'bbbb@gmail.com', '111111112', 2, 23, '고려대학교', sysdate(), '[
    ["j", 2.4401],
    [" ", 3.0000],
    ["i", 1.0433],
    ["i", 2.6569],
    ["j", 2.1122]
]');

SELECT * FROM `pack`;
SELECT * FROM `reply`;
SELECT p.*, r.count FROM pack p LEFT JOIN (SELECT p_id, COUNT(*) count FROM reply GROUP BY p_id) r ON p.p_id=r.p_id;