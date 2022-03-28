-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema DojoChat_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `DojoChat_schema` ;

-- -----------------------------------------------------
-- Schema DojoChat_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DojoChat_schema` DEFAULT CHARACTER SET utf8 ;
USE `DojoChat_schema` ;

-- -----------------------------------------------------
-- Table `DojoChat_schema`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DojoChat_schema`.`users` ;

CREATE TABLE IF NOT EXISTS `DojoChat_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `username` VARCHAR(255) NULL,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() on UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DojoChat_schema`.`rooms`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DojoChat_schema`.`rooms` ;

CREATE TABLE IF NOT EXISTS `DojoChat_schema`.`rooms` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now() on UPDATE Now(),
  `administrator_id` INT NOT NULL,
  `number` INT NOT NULL,
  `passkey` VARCHAR(45) NULL,
  PRIMARY KEY (`id`, `administrator_id`, `number`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DojoChat_schema`.`members`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DojoChat_schema`.`members` ;

CREATE TABLE IF NOT EXISTS `DojoChat_schema`.`members` (
  `members_id` INT NOT NULL AUTO_INCREMENT,
  `room_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`members_id`, `room_id`, `user_id`),
  INDEX `fk_rooms_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_rooms_has_users_rooms1_idx` (`room_id` ASC, `members_id` ASC) VISIBLE,
  CONSTRAINT `fk_rooms_has_users_rooms1`
    FOREIGN KEY (`room_id` , `members_id`)
    REFERENCES `DojoChat_schema`.`rooms` (`id` , `administrator_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rooms_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `DojoChat_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DojoChat_schema`.`chats`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DojoChat_schema`.`chats` ;

CREATE TABLE IF NOT EXISTS `DojoChat_schema`.`chats` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now() on UPDATE Now(),
  `room_id` INT NOT NULL,
  PRIMARY KEY (`id`, `room_id`),
  INDEX `fk_chats_rooms1_idx` (`room_id` ASC) VISIBLE,
  CONSTRAINT `fk_chats_rooms1`
    FOREIGN KEY (`room_id`)
    REFERENCES `DojoChat_schema`.`rooms` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DojoChat_schema`.`messages`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DojoChat_schema`.`messages` ;

CREATE TABLE IF NOT EXISTS `DojoChat_schema`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT Now(),
  `updated_at` DATETIME NULL DEFAULT Now() on UPDATE Now(),
  `chat_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `chat_id`, `user_id`),
  INDEX `fk_messages_chats1_idx` (`chat_id` ASC) VISIBLE,
  INDEX `fk_messages_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_chats1`
    FOREIGN KEY (`chat_id`)
    REFERENCES `DojoChat_schema`.`chats` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `DojoChat_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
