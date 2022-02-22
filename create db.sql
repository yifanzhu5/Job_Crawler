CREATE TABLE `job`.`jobs` (
  `title` TEXT NOT NULL,
  `publish_time` INT NULL,
  `description` TEXT NULL,
  `company` TEXT NOT NULL,
  `locations` TEXT NULL,
  `apply_url` TEXT NULL,
  `from_url` VARCHAR(600) NOT NULL,
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
  PRIMARY KEY (`id`),
  UNIQUE INDEX `from_url_UNIQUE` (`from_url` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;
