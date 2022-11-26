CREATE TABLE `log`
(
    `id`          int NOT NULL AUTO_INCREMENT,
    `datasource`  varchar(500) DEFAULT NULL,
    `timestamp`   datetime     DEFAULT NULL,
    `remote_addr` varchar(500) DEFAULT NULL,
    `path`        varchar(500) DEFAULT NULL,
    `status`      varchar(500) DEFAULT NULL,
    `protocol`    varchar(500) DEFAULT NULL,
    `method`      varchar(500) DEFAULT NULL,
    `user_agent`  varchar(500) DEFAULT NULL,
    `type`        varchar(20)  DEFAULT NULL,
    `created_at`  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    `updated_at`  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY           `idx_datasource_timestamp` (`datasource`,`timestamp`) USING BTREE,
    KEY           `idx_timestamp` (`timestamp`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
