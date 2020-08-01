-- ----------------------------
-- Table structure for lucky_numbers
-- ----------------------------
DROP TABLE IF EXISTS `lucky_numbers`;
CREATE TABLE `lucky_numbers` (
  `date` date NOT NULL,
  `blue` varchar(255) DEFAULT NULL,
  `red` varchar(255) DEFAULT NULL,
  `isBuyed` char(1) DEFAULT '0',
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
