
// 政策咨询表

//publish VARCHAR(50) COMMENT '公布日期',
                    expiry VARCHAR(50) COMMENT '施行日期',
                    office VARCHAR(50) COMMENT '制定机关',
                    title VARCHAR(255) COMMENT '标题',
                    type VARCHAR(50) COMMENT '类型',

CREATE TABLE `consultation`  (
                             `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
                             `type` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '类型',
                             `title` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '标题',
                             `content` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '内容',
                             `publish` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '发布日期',
                             `expiry` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '施行日期',
                             `office` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '制定机关',
                             `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '外部链接',
                             `attachment` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '附件',
                             `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
                             PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB  CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '政策咨询' ROW_FORMAT = COMPACT;
alter table consultation add `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '来源';
alter table law add `status` tinyint(2) UNSIGNED NOT NULL DEFAULT 1 COMMENT '0 无效,1 有效 时效性';
alter table law add `level` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '法律效力位阶';

