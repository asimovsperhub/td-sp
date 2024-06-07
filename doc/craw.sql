CREATE TABLE bidding_information(
id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'UID',
bulletin_type VARCHAR(50)  COMMENT '公告类型',
notice_nature  VARCHAR(50)  COMMENT '公告性质',
city VARCHAR(50) COMMENT '所属城市',
industry_classification VARCHAR(50) COMMENT '行业分类',
release_time VARCHAR(50) COMMENT '发布时间',
bidopening_time  VARCHAR(50) COMMENT '开标时间',
title VARCHAR(255) COMMENT '标题',
announcement_content LongText COMMENT '公告内容',
attachment  VARCHAR(255) COMMENT '招标附件',
amount VARCHAR(255) COMMENT '金额',
contact_person VARCHAR(255) COMMENT '联系人',
contact_information  VARCHAR(255) COMMENT '联系方式',
contact_content  VARCHAR(255)  COMMENT '联系方式内容',
`created_at` datetime NULL DEFAULT NULL COMMENT '创建日期',
link   VARCHAR(255) COMMENT '源链接'
);


--`notice_nature` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '公告性质',
--FULLTEXT INDEX `announcement` (`announcement_content`)
--crawldata
--ALTER TABLE bidding ADD FULLTEXT INDEX title(title);
--ALTER TABLE bidding ADD FULLTEXT INDEX title_announcement(title,announcement_content);



--自然语言模式 ( IN NATURAL LANGUAGEMODE )
--
--遵从自然语言分词规则，匹配完整的单词，查询关键字也会根据分词规则自动分词，只要匹配分词后的各个单词中其中任意一个便可以查询到记录，默认就是这种模式
--
--where 条件后接 MATCH(column_name1,column_name2) AGAINST('keyword')
--#或者
--where 条件后接 MATCH(column_name1,column_name2) AGAINST('keyword' IN NATURAL LANGUAGE MODE)
--eg1. MATCH(food_name) AGAINST('apple') 可以匹配出 apple，apples，Apples 等完整单词
--
--eg2. MATCH(food_name) AGAINST('apple orange') 可以匹配出 apple，apples，Apples 、orange、oranges、Oranges等完整单词
--
--布尔全文搜索 （ IN BOOLEAN MODE ）
--
--如果在AAGAINST()函数中指定了IN BOOLEN MODE模式，则MySQL会执行布尔全文搜索。在该搜索模式下，待搜索单词前或后的一些特定字符会有特殊的含义。
--
--where 条件后接 MATCH(column_name1,column_name2) AGAINST('keyword' IN BOOLEAN MODE)


CREATE TABLE `bidding`  (
                                  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
                                  `bulletin_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '公告类型',
                                  `city` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '所属城市',
                                  `industry_classification` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '行业分类',
                                  `release_time` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '发布时间',
                                  `bidopening_time` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '开标时间',
                                  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '标题',
                                  `abstract` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '摘要',
                                  `enterprise` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '企业信息',
                                  `announcement_content` LongText CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '公告内容',
                                  `link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '源链接',
                                  `attachment` char(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '招标附件',
                                  `amount` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '金额',
                                  `contact_person` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '联系人',
                                  `contact_information` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '联系方式',
                                  `created_at` datetime NULL DEFAULT NULL COMMENT '爬取日期',
                                  PRIMARY KEY (`id`) USING BTREE,
                                  INDEX `bulletin` (`bulletin_type`) USING BTREE,
                                  INDEX `city`(`city`) USING BTREE,
                                  INDEX `industry`(`industry_classification`) USING BTREE,
                                  INDEX `release`(`release_time`) USING BTREE,
                                  INDEX `bidopening`(`bidopening_time`) USING BTREE,
                                  INDEX `created`(`created_at`) USING BTREE,
                                  INDEX `title`(`title`) USING BTREE,
                                  INDEX `bulletin_city`(`bulletin_type`,`city`) USING BTREE,
                                  INDEX `bulletin_city_industry`(`bulletin_type`,`city`,`industry_classification`) USING BTREE,
                                  INDEX `bulletin_city_industry_release`(`bulletin_type`,`city`,`industry_classification`,`release_time`) USING BTREE
) ENGINE = InnoDB  CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '招标信息' ROW_FORMAT = DYNAMIC;
alter table bidding MODIFY `abstract` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '摘要';
alter table bidding MODIFY `attachment` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '招标附件';

// 新增列
alter table bidding add `bid_amount` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '中标金额';
alter table bidding add `tender_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '招标企业';
alter table bidding add `win_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '中标企业';

ALTER TABLE bidding ADD FULLTEXT INDEX enterprise(enterprise);
ALTER TABLE bidding MODIFY `attachment` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '招标附件',