## Bug Report

Please answer these questions before submitting your issue. Thanks!

1. What did you do?
If possible, provide a recipe for reproducing the error.

```
$ bin/sync_diff_inspector --config ~/Projects/ticdc/dm/tests/all_mode/conf/diff_config.toml
A total of 2 tables need to be compared

Comparing the table structure of ``all_mode`.`t1`` ... equivalent
Comparing the table data of ``all_mode`.`t1`` ... equivalent
Comparing the table structure of ``all_mode`.`t2`` ... equivalent
Comparing the table data of ``all_mode`.`t2`` ... equivalent
_____________________________________________________________________________
Progress [============================================================>] 100% 0/Progress [============================================================>] 100% 0/0
A total of 2 table have been compared and all are equal.
You can view the comparision details through '/tmp/ticdc_dm_test/output/sync_diff.log'
```

2. What did you expect to see?

table structure is not equal, because in 3306

```
MySQL [all_mode]> show create table t1;
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `dt` datetime DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

in 4000

```
MySQL [all_mode]> show create table t1;
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                                                                                                           |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `dt` datetime DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30004 |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```


3. What did you see instead?


4. What version of TiDB are you using (`tidb-server -V` or run `select tidb_version();` on TiDB)?

5. which tool are you using?

6. what versionof tool are you using (`pump -V` or `tidb-lightning -V` or `syncer -V`)?
