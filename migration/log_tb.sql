CREATE TABLE `log_tb` (
  `uuid` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `remote_addr` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `protocol` varchar(255) NOT NULL,
  `method` varchar(255) NOT NULL,
  `user_agent` text NOT NULL,
  `datasource` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX `idx_datasource_timestamp` ON log_tb (`datasource`, `timestamp`);
CREATE INDEX `idx_timestamp` ON log_tb (`timestamp`);

ALTER TABLE log_tb
ADD COLUMN `type` varchar(30) DEFAULT NULL AFTER datasource;

ALTER TABLE log_tb
MODIFY COLUMN `path` text DEFAULT NULL;

ALTER TABLE log_tb
MODIFY COLUMN `user_agent` text DEFAULT NULL;