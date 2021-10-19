/*
 Navicat Premium Data Transfer

 Source Server         : 本地库
 Source Server Type    : MySQL
 Source Server Version : 80022
 Source Host           : localhost:3306
 Source Schema         : stock_db

 Target Server Type    : MySQL
 Target Server Version : 80022
 File Encoding         : 65001

 Date: 19/10/2021 15:31:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for fund_focus
-- ----------------------------
DROP TABLE IF EXISTS `fund_focus`;
CREATE TABLE `fund_focus` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `note_info` varchar(200) DEFAULT '',
  `info_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `info_id` (`info_id`) USING BTREE,
  CONSTRAINT `FK_DNO` FOREIGN KEY (`info_id`) REFERENCES `fund_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
