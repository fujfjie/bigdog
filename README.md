# bigdog
调度项目
>依赖关系图:
>>![](/total.png "")

>后端表配置：
>>数据库链接配置请调整：dbConfig
>>后端表结构
>>>db：metadata，
CREATE DATABASE metadata CHARSET utf8 COLLATE utf8_general_ci;
>>>员工信息表
 CREATE TABLE metadata.`bigdog_staff_info` (
  `staff_id` int(11) NOT NULL COMMENT '员工ID',
  `staff_name` varchar(64) COLLATE utf8_bin DEFAULT NULL COMMENT '员工名称',
  `staff_mail` varchar(128) COLLATE utf8_bin DEFAULT NULL COMMENT '员工邮箱',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='员工信息表';

>>>规则 信息表
CREATE TABLE metadata.`bigdog_rule_info` (
  `rule_id` int(11) NOT NULL COMMENT '规则ID',
  `rule_name` varchar(64) COLLATE utf8_bin DEFAULT NULL COMMENT '规则名称',
  `rule_desc` varchar(256) COLLATE utf8_bin DEFAULT NULL COMMENT '规则描述',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='规则 信息表';
INSERT INTO `bigdog_rule_info` VALUES ('10001', 'DAY', '按天都执行', now());
INSERT INTO `bigdog_rule_info` VALUES ('10002', 'ODDDAY', '逢单执行', now());
INSERT INTO `bigdog_rule_info` VALUES ('10003', 'EVENDAY', '逢双执行', now());
INSERT INTO `bigdog_rule_info` VALUES ('10004', 'LASTDAY', '月末最后一天执行', now());
INSERT INTO `bigdog_rule_info` VALUES ('10005', 'FIRSTDAY', '月初第一天执行', now());
INSERT INTO `bigdog_rule_info` VALUES ('10006', 'WORKDAY', '周一至周五每天执行', now());
INSERT INTO `bigdog_rule_info` VALUES ('10007', 'WEEK', '周', now());
INSERT INTO `bigdog_rule_info` VALUES ('10008', 'MONTH', '月', now());
INSERT INTO `bigdog_rule_info` VALUES ('10009', 'HOUR', '时', now());

>>>发送邮件账户, 注意 dbConfig文件中SQLDICT['pushMailInfo']的program_name写死为bigdog
CREATE TABLE metadata.`meta_push_mail` (
  `program_id` int(11) NOT NULL AUTO_INCREMENT,
  `program_name` varchar(64) NOT NULL COMMENT '程序工程名称',
  `mail_host` varchar(64) NOT NULL COMMENT '邮件host',
  `mail_user` varchar(64) NOT NULL COMMENT '邮件用户',
  `mail_user_head` varchar(64) DEFAULT NULL COMMENT '邮件头名称',
  `mail_user_password` varchar(64) NOT NULL COMMENT '邮件密码',
  `mail_port` int(11) NOT NULL COMMENT '端口',
  `mail_subject` varchar(255) DEFAULT NULL COMMENT '告警主题',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`program_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10005 DEFAULT CHARSET=utf8 COMMENT='发送邮件账户';

>>>调度组信息表
CREATE TABLE metadata.`bigdog_group_info` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '组ID',
  `group_name` varchar(64) COLLATE utf8_bin DEFAULT NULL COMMENT '组名称',
  `group_desc` varchar(256) COLLATE utf8_bin DEFAULT NULL COMMENT '组描述',
  `retry_count` int(11) DEFAULT NULL COMMENT 'job异常，重试次数',
  `parallel_nums` int(11) DEFAULT NULL COMMENT '并发次数',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `status_id` int(11) DEFAULT '0' COMMENT '状态ID 0 正常 1 异常',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=199902 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='调度组信息表';

>>>员工与调度组关系表
CREATE TABLE metadata.`bigdog_group_staff_rela` (
  `group_id` int(11) DEFAULT NULL COMMENT '组ID',
  `staff_id` int(11) DEFAULT NULL COMMENT '员工ID',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  UNIQUE KEY `fk_meta_group_staff` (`group_id`,`staff_id`),
  KEY `fk_meta_group_staff_staff` (`staff_id`),
  CONSTRAINT `fk_meta_group_staff_group` FOREIGN KEY (`group_id`) REFERENCES `bigdog_group_info` (`group_id`),
  CONSTRAINT `fk_meta_group_staff_staff` FOREIGN KEY (`staff_id`) REFERENCES `bigdog_staff_info` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='员工与组关系表';

>>>job信息表
CREATE TABLE metadata.`bigdog_job_info` (
  `group_id` int(11) DEFAULT NULL COMMENT '组信息ID -- bigdog.meta_group_info',
  `job_id` int(11) NOT NULL COMMENT 'JOB ID',
  `job_name` varchar(64) COLLATE utf8_bin DEFAULT NULL COMMENT 'JOB 名称',
  `job_desc` varchar(256) COLLATE utf8_bin DEFAULT NULL COMMENT 'JOB 描述',
  `job_path` varchar(500) COLLATE utf8_bin DEFAULT NULL COMMENT 'job路径 -- 只支持sh脚本',
  `rule_id` int(11) DEFAULT '10001' COMMENT '规则ID -- bigdog.meta_RULE_info',
  `EXECUTE_TIME` varchar(32) COLLATE utf8_bin DEFAULT '0:00:00' COMMENT '时间依赖',
  `RETRY_COUNT` int(11) DEFAULT '2' COMMENT '重试次数',
  `EXECUTE_DAY` varchar(128) COLLATE utf8_bin DEFAULT NULL COMMENT '周月时间[1,2,3,4,5,6,7],[1,2,3,4,5,6,7,8,9,......28,29,30,31]',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `STATUS_ID` int(11) DEFAULT '0' COMMENT '状态ID 0 正常 1 异常',
  PRIMARY KEY (`job_id`),
  UNIQUE KEY `uk_job_name` (`job_name`) USING BTREE,
  KEY `fk_meta_job_info_group_id` (`group_id`),
  KEY `fk_meta_job_info_rule_id` (`rule_id`),
  CONSTRAINT `fk_meta_job_info_group_id` FOREIGN KEY (`group_id`) REFERENCES `bigdog_group_info` (`group_id`),
  CONSTRAINT `fk_meta_job_info_rule_id` FOREIGN KEY (`rule_id`) REFERENCES `bigdog_rule_info` (`rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='job信息表';

>>>job 关系表
CREATE TABLE metadata.`bigdog_job_rela` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_job_id` int(11) DEFAULT NULL COMMENT '开始jobid',
  `end_job_id` int(11) NOT NULL COMMENT '结束jobid',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_meta_job_rela` (`start_job_id`,`end_job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='job 关系表';

>>>job与员工关系表,若未配置异常将发送给调度用户
CREATE TABLE metadata.`bigdog_job_staff_rela` (
  `job_id` int(11) DEFAULT NULL COMMENT 'job ID',
  `staff_id` int(11) DEFAULT NULL COMMENT '员工ID',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  KEY `fk_meta_job_staff_rela_job` (`job_id`),
  KEY `fk_meta_job_staff_rela_staff` (`staff_id`),
  CONSTRAINT `fk_meta_job_staff_rela_job` FOREIGN KEY (`job_id`) REFERENCES `bigdog_job_info` (`job_id`),
  CONSTRAINT `fk_meta_job_staff_rela_staff` FOREIGN KEY (`staff_id`) REFERENCES `bigdog_staff_info` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='job与员工关系表';

>>>调度组日志信息表
CREATE TABLE metadata.`bigdog_log_group_info` (
  `group_id` int(11) DEFAULT NULL COMMENT '组ID',
  `record_day` int(11) DEFAULT NULL COMMENT '记录日期',
  `snapshot` varchar(32) COLLATE utf8_bin DEFAULT NULL COMMENT '快照',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `status` int(11) DEFAULT NULL COMMENT '状态 1 开始 2 正常 3 错误 4 异常拉起',
  `conf_pv` int(11) DEFAULT NULL COMMENT '任务信息表 配置任务个数',
  `real_pv` int(11) DEFAULT NULL COMMENT '任务关系表 配置任务个数',
  `succ_pv` int(11) DEFAULT NULL COMMENT '成功任务个数',
  `err_pv` int(11) DEFAULT NULL COMMENT '失败人数个数'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='组日志信息表';

>>>job日志信息表
CREATE TABLE metadata.`bigdog_log_job_info` (
  `group_id` int(11) NOT NULL COMMENT '组ID',
  `job_id` int(11) NOT NULL COMMENT 'JOBID',
  `record_day` int(11) NOT NULL COMMENT '记录日期',
  `snapshot` varchar(32) COLLATE utf8_bin NOT NULL COMMENT '快照',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `status` int(11) DEFAULT NULL COMMENT '状态 1 开始 2 成功 3 错误',
  `error_code` varchar(32) COLLATE utf8_bin DEFAULT NULL COMMENT '错误代码',
  `crontab_time` datetime DEFAULT NULL COMMENT '定时任务时间',
  `execute_step` int(11) NOT NULL COMMENT '重试次数',
  `log_path` varchar(256) COLLATE utf8_bin DEFAULT NULL COMMENT '日志路径',
  PRIMARY KEY (`job_id`,`snapshot`,`group_id`,`record_day`,`execute_step`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='job日志信息表';

>>>试图 job与员工聚合表
CREATE VIEW metadata.bigdog_view_job_staff_rela AS
SELECT b.job_id AS job_id,
       group_concat(a.staff_mail SEPARATOR ',') AS mail_list
  FROM metadata.bigdog_job_staff_rela b
  JOIN
       metadata.bigdog_staff_info a
  ON (a.staff_id = b.staff_id)
 GROUP BY b.job_id

>>>试图 调度组与员工聚合表
CREATE VIEW metadata.bigdog_view_group_staff_rela AS
SELECT b.group_id AS group_id,
       group_concat(a.staff_mail SEPARATOR ',') AS mail_list
  FROM metadata.bigdog_group_staff_rela b
  JOIN
       metadata.bigdog_staff_info a
  ON (b.staff_id = a.staff_id)
 GROUP BY b.group_id

>>>试图 job信息表
CREATE VIEW metadata.bigdog_view_job_info AS
SELECT a.group_id AS group_id,
       a.job_id AS job_id,
       a.job_name AS job_name,
       a.job_path AS job_path,
       a.EXECUTE_TIME AS execute_time,
       a.EXECUTE_DAY AS execute_day,
       a.RETRY_COUNT AS retry_count,
       c.rule_name AS rule_name,
       d.mail_list AS mail_list
  FROM metadata.bigdog_job_info a
  JOIN
       metadata.bigdog_group_info b
  ON (a.group_id = b.group_id)
  JOIN
       metadata.bigdog_rule_info c
  ON (a.rule_id = c.rule_id)
  LEFT OUTER JOIN
       metadata.bigdog_view_job_staff_rela d
  ON (a.job_id = d.job_id)
 WHERE a.status_id = 0
   AND b.status_id = 0

>>>试图 job关系
CREATE VIEW bigdog_view_job_rela AS
SELECT CASE WHEN a.start_job_id = '' OR a.start_job_id = 0 THEN NULL ELSE a.start_job_id END AS start_job_id,
       a.end_job_id AS end_job_id,
       CASE WHEN b.group_id IS NOT NULL THEN b.group_id ELSE c.group_id END AS group_id
  FROM metadata.bigdog_job_rela a
  LEFT OUTER JOIN
       metadata.bigdog_job_info b
  ON (a.end_job_id = b.job_id)
  LEFT OUTER JOIN
       metadata.bigdog_job_info c
  ON (a.start_job_id = c.job_id)