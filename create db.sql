CREATE TABLE `job`.`jobs` (
  `glassdoor_id` TEXT NULL,
  `title` TEXT NOT NULL,
  `publish_time` INT NULL,
  `description` LONGTEXT NULL,
  `company` TEXT NOT NULL,
  `locations` TEXT NULL,
  `apply_url` LONGTEXT NULL,
  `from_url` LONGTEXT NOT NULL,
  `basic_qualifications` TEXT NULL,
  `team` TEXT NULL,
  `city` TEXT NULL,
  `job_category` TEXT NULL,
  `job_family` TEXT NULL,
  `job_schedule_type` TEXT NULL,
  `preferred_qualifications` TEXT NULL,
  `update_time` TEXT NULL,
  `new_grad` TINYINT(1) NULL,
  `has_remote` TINYINT(1) NULL,
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `subcompany` TEXT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


