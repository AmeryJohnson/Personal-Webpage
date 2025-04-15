CREATE TABLE IF NOT EXISTS experiences (
`experience_id`      int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'PK:The experience id',
`position_id`        int(11)       NOT NULL 				COMMENT 'FK:The position id',
`name`               varchar(100)  NOT NULL					COMMENT 'Name of experience',
`description`        varchar(500)  DEFAULT NULL                 COMMENT 'Description of experience',
`hyperlink`          varchar(500)  DEFAULT NULL                COMMENT 'Hyperlink for experience',
`start_date`         varchar(100)  DEFAULT NULL                 COMMENT 'Start date of experience',
`end_date`           varchar(100)  DEFAULT NULL                 COMMENT 'End date of experience',
PRIMARY KEY (`experience_id`),
FOREIGN KEY (`position_id`) REFERENCES positions(`position_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Experiences I have had";