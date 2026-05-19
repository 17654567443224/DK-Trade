/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80034 (8.0.34)
 Source Host           : localhost:3306
 Source Schema         : dk-qaunt

 Target Server Type    : MySQL
 Target Server Version : 80034 (8.0.34)
 File Encoding         : 65001

 Date: 15/02/2025 03:47:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for strategy_generate_report
-- ----------------------------
DROP TABLE IF EXISTS `strategy_generate_report`;
CREATE TABLE `strategy_generate_report`  (
  `id` bigint NOT NULL COMMENT '策略ID',
  `final_balance` double NOT NULL COMMENT '余额',
  `max_drawdown` double NOT NULL COMMENT '最大回撤',
  `win_rate` double NOT NULL COMMENT '胜率',
  `max_profit` double NOT NULL COMMENT '最大盈利',
  `max_loss` double NOT NULL COMMENT '最大亏损',
  `total_trades` int NOT NULL COMMENT '交易总数',
  `sharpe_ratio` double NOT NULL COMMENT '夏普比率',
  `annualized_return` double NOT NULL COMMENT '年化',
  `total_pnlRatio` double NOT NULL COMMENT '总收益率',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
