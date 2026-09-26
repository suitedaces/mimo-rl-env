## Bug Report

Please answer these questions before submitting your issue. Thanks!

### 1. Minimal reproduce step (Required)


```
 set global tidb_gogc_tuner_max_value=500;
 show warning;
```
<!-- a step by step guide for reproducing the bug. -->

### 2. What did you expect to see? (Required)
None 
### 3. What did you see instead (Required)

| Level   | Code | Message                                                    |
+---------+------+------------------------------------------------------------+
| Warning | 1292 | Truncated incorrect tidb_gogc_tuner_max_value value: '500' |
+---------+------+------------------------------------------------------------+

### 4. What is your TiDB version? (Required)

<!-- Paste the output of SELECT tidb_version() -->
