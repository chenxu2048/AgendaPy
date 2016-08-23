DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `userId` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户特征id',
  `username` varchar(64) NOT NULL COMMENT '用户名',
  `password` char(32) NOT NULL COMMENT '用户密码，md5值',
  `email` varchar(128) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(32) DEFAULT NULL COMMENT '电话',
  PRIMARY KEY (`userId`),
  UNIQUE KEY (`username`)
) AUTO_INCREMENT = 0, DEFAULT CHARSET=utf8, COMMENT '用户信息表';
