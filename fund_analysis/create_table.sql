 CREATE TABLE `all_funds` (
  `code_id` char(6) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


 CREATE TABLE `fund_achievement` (
  `date` date NOT NULL,
  `code_id` char(6) NOT NULL,
  `scale` float(16),
	`week1` float(16),
	`month1` float(16),
	`month3` float(16),
	`month6` float(16),
	`year1` float(16),
	`year3` float(16),
  PRIMARY KEY (`date`,`code_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;