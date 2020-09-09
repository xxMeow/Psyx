SHOW DATABASES;

DROP DATABASE psyx;

CREATE DATABASE psyx;
USE psyx;
SHOW TABLES;

DROP TABLE IF EXISTS `pack`;
DROP TABLE IF EXISTS `reply`;

CREATE TABLE `pack` (
    `p_id` INT NOT NULL AUTO_INCREMENT,
    `gender` TINYINT NOT NULL,
    `age_low` TINYINT NOT NULL,
    `age_high` TINYINT NOT NULL,
    `name` CHAR(32) NOT NULL UNIQUE, 
    `date` DATETIME NOT NULL,
    PRIMARY KEY (`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `reply` (
    `r_id` INT NOT NULL AUTO_INCREMENT,
    `p_id` INT NOT NULL,
    `mail` CHAR(48) NOT NULL,
    `student_no` CHAR(16) NOT NULL,
    `gender` TINYINT NOT NULL,
    `age` TINYINT NOT NULL,
    `affiliation` CHAR(48) NOT NULL,
    `date` DATETIME NOT NULL,
    `answer` JSON NOT NULL,
    PRIMARY KEY (`r_id`),
    FOREIGN KEY (`p_id`) REFERENCES `pack`(`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DESCRIBE pack;
DESCRIBE reply;

INSERT INTO `pack` VALUES (NULL, 1, 20, 30, 'animal', sysdate());
INSERT INTO `reply` VALUES (NULL, 1, 'aaaa@gmail.com', '111111111', 1, 25, '고려대학교', sysdate(), '[
    ["j", 2.4401],
    ["x", 3.0000],
    ["i", 1.0433],
    ["i", 2.6569],
    ["j", 2.1122]
]');
INSERT INTO `reply` VALUES (NULL, 2, 'aaaa@gmail.com', '111111111', 1, 25, '고려대학교', sysdate(), '[
    ["j", 2.4401],
    ["x", 3.0000],
    ["i", 1.0433],
    ["i", 2.6569],
    ["j", 2.1122]
]');

SELECT * FROM `pack`;
SELECT * FROM `reply`;
