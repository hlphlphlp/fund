 CREATE TABLE `shanghai_index` (
   `id` int(16) NOT NULL AUTO_INCREMENT,
   `code_id` char(6) DEFAULT NULL COMMENT '指数代码',
   `name` varchar(64) DEFAULT NULL COMMENT '指数名称',
   `current_value` FLOAT(64,2) DEFAULT NULL COMMENT '当前点数',
   `yesterday_end` FLOAT(64,2) DEFAULT NULL COMMENT '昨天收盘点数',
   `today_begin` FLOAT(64,2) DEFAULT NULL COMMENT '当天开盘点数',
   `today_highest` FLOAT(64,2) DEFAULT NULL COMMENT '今日最高点',
   `today_lowest` FLOAT(64,2) DEFAULT NULL COMMENT '今日最低点',
   `deal_count` FLOAT(64,2) DEFAULT NULL COMMENT '成交量： 亿手',
   `compare_to_yesterday` FLOAT(64,2) DEFAULT NULL COMMENT '与昨天点数相比',
   `amplitude` FLOAT(64,2) DEFAULT NULL COMMENT '涨/降幅度： %',
  `deal_money` FLOAT(64,2) DEFAULT NULL COMMENT '单位：亿元',
   `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `index_line` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `low` int(16) DEFAULT NULL,
  `high` int(16) DEFAULT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

 CREATE TABLE `fund_info` (
  `code_id` char(6) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `useful` char(1) DEFAULT '1' COMMENT '0-无用， 1-优秀种子-未买，2-买了',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `manager_id` INT(4) DEFAULT NULL,
  `worth_to_buy` float(8,4) DEFAULT NULL,
  `worth_to_sell` float(8,4) DEFAULT NULL,
  PRIMARY KEY (`code_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



 CREATE TABLE `stock_info` (
  `code_id` char(6) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `useful` char(1) DEFAULT '1' COMMENT '0-无用， 1-有用，2-优秀种子（未买）',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `manager_id` INT(4) DEFAULT NULL,
  `worth_to_buy` float(8,4) DEFAULT NULL,
  `worth_to_sell` float(8,4) DEFAULT NULL,
  PRIMARY KEY (`code_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



 CREATE TABLE `mail_sender` (
   `id` int(16) NOT NULL AUTO_INCREMENT,
  `user` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


 CREATE TABLE `mail_to` (
   `id` int(16) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


 CREATE TABLE `s_content` (
   `id` int(16) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `content` text,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
