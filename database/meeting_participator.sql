DROP TABLE IF EXISTS `meetingMember`;

CREATE TABLE `meetingMember`(
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '会议参与者的标识id，唯一',
  `userId` bigint(20) unsigned NOT NULL COMMENT '用户的id',
  `meetingId` bigint(20) unsigned NOT NULL COMMENT '参与会议id',
  `role` enum('sponsor', 'participator') NOT NULL DEFAULT 'participator' COMMENT'会议角色',
  PRIMARY KEY (`id`),
  FOREIGN KEY (`userId`) REFERENCES user(`userId`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`meetingId`) REFERENCES meeting(`meetingId`) ON DELETE CASCADE ON UPDATE CASCADE
) AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT '会议参与表';
