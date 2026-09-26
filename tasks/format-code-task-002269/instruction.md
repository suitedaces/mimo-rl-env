## Bug Report

Please answer these questions before submitting your issue. Thanks!

### 1. Minimal reproduce step (Required)
``` sql
select greatest(cast("2020-01-01 01:01:01" as datetime), cast("2019-01-01 01:01:01" as datetime) )union select null;
```

### 2. What did you expect to see? (Required)
``` sql
mysql> select greatest(cast("2020-01-01 01:01:01" as datetime), cast("2019-01-01 01:01:01" as datetime) )union select null;

+---------------------------------------------------------------------------------------------+
| greatest(cast("2020-01-01 01:01:01" as datetime), cast("2019-01-01 01:01:01" as datetime) ) |
+---------------------------------------------------------------------------------------------+
| 2020-01-01 01:01:01                                                                         |
| NULL                                                                                        |
+---------------------------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

### 3. What did you see instead (Required)

``` sql
tidb> select greatest(cast("2020-01-01 01:01:01" as datetime), cast("2019-01-01 01:01:01" as datetime) )union select null;

+---------------------------------------------------------------------------------------------+
| greatest(cast("2020-01-01 01:01:01" as datetime), cast("2019-01-01 01:01:01" as datetime) ) |
+---------------------------------------------------------------------------------------------+
| NULL                                                                                        |
|                                                                                             |
+---------------------------------------------------------------------------------------------+
2 rows in set, 1 warning (0.01 sec)
```

### 4. What is your TiDB version? (Required)

a4146033fb6deec464de9faf5f5412b87ef5d06c
