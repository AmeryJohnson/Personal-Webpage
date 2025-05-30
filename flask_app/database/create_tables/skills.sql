CREATE TABLE IF NOT EXISTS skills (
`skill_id`             int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'PK:The skill id',
`experience_id`        int(11)       NOT NULL                   COMMENT 'FK:The experience id',
`name`                 varchar(100)  NOT NULL                   COMMENT 'Name of the skill',
`skill_level`          int(2)        NOT NULL                   COMMENT 'Level of skill 1 through 10',
PRIMARY KEY (`skill_id`),
FOREIGN KEY (`experience_id`) REFERENCES experiences(`experience_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Skills earned through each experience";