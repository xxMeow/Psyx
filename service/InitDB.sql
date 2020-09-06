CREATE DATABASE psyx;

USE psyx;

DROP TABLE IF EXISTS `pack`;
DROP TABLE IF EXISTS `reply`;
/*
CREATE DATABASE IF NOT EXISTS `pack`;
CREATE DATABASE IF NOT EXISTS `reply`;
*/

CREATE TABLE `pack` (
    `p_id` INT NOT NULL AUTO_INCREMENT,
    `gender` TINYINT NOT NULL,
    `age_low` TINYINT NOT NULL,
    `age_high` TINYINT NOT NULL,
    `name` CHAR(32) NOT NULL UNIQUE, 
    `date` DATETIME NOT NULL,
    PRIMARY KEY (`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `pack` VALUES (0, 1, 20, 30, 'catdog', sysdate());

CREATE TABLE `reply` (
    `r_id` INT NOT NULL AUTO_INCREMENT,
    `p_id` INT NOT NULL,
    `mail` CHAR(48) NOT NULL,
    `student_no` CHAR(16) NOT NULL,
    `gender` TINYINT NOT NULL,
    `affiliation` CHAR(48) NOT NULL,
    `date` DATETIME NOT NULL,
    `answer` JSON NOT NULL,
    PRIMARY KEY (`r_id`),
    FOREIGN KEY (`p_id`) REFERENCES `pack`(`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `reply` VALUES (NULL, 'aaaa@gmail.com', '111111111', 1, sysdate(), '0000000000');
INSERT INTO `reply` VALUES (NULL, 'bbbb@naver.com', '222222222', 1, sysdate(), '0000000001');
INSERT INTO `reply` VALUES (NULL, 'cccc@gmail.com', '333333333', 2, sysdate(), '0000000011');
INSERT INTO `reply` VALUES (NULL, 'dddd@naver.com', '444444444', 1, sysdate(), '0000000111');

SELECT * FROM `reply`;
