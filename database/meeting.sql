DROP TABLE IF EXISTS `meeting`;

CREATE TABLE `meeting` (
  `meetingId` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '会议唯一标识id',
  `startDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '会议开始时间',
  `endDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '会议结束时间',
  `title` varchar(128) NOT NULL COMMENT '会议标题，唯一',
  PRIMARY KEY (`meetingId`),
  UNIQUE KEY `title` (`title`)
) AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='会议信息表';
