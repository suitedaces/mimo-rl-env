Flyway query on information schema stopped working
#### Overview of the Issue

In my company we're using the `vttestserver` docker image with testcontainers and flyway for the acceptance test (a simple 1 shard 1 keyspace approach).
Since a few days ago (we noticed it on Friday 27 Aug 2021), one of the queries Flyway performs to verify if our database exists fails all the time.

```
SELECT (SELECT 1 FROM information_schema.schemata WHERE schema_name='MyDatabase' LIMIT 1);
```

#### Reproduction Steps

Steps to reproduce this issue:

1. `docker run -p 3306:33577 -e PORT=33574 -e KEYSPACES="MyDatabase" -e NUM_SHARDS="1" -e MYSQL_BIND_HOST=0.0.0.0 vitess/vttestserver:mysql80`
2. execute the query above

(fails also with `vitess/vttestserver:mysql57`, works fine with vanilla `mysql:8.0`.

#### Operating system and Environment details

OS, Architecture, and any other information you can provide about the environment.

- Operating system (output of `cat /etc/os-release`): tried on ubuntu 21, OSX 11 and CentOS
- Kernel version (output of `uname -sr`): Linux 5.11.0-31-generic
- Architecture (output of `uname -m`): x86_64

#### Log Fragments

on mysql:
```
mysql> SELECT (SELECT 1 FROM information_schema.schemata WHERE schema_name='MyDatabase' LIMIT 1);
ERROR 1105 (HY000): target: MyDatabase.0.primary: vttablet: rpc error: code = InvalidArgument desc = missing bind var __vtschemaname (CallerID: userData1)
```

from the container:
```
: Sql: "select (select :vtg1 from information_schema.schemata where schema_name = :__vtschemaname limit :vtg1) from dual", BindVars: {#maxLimit: "type:INT64 value:\"10001\""vtg1: "type:INT64 value:\"1\""vtg2: "type:VARBINARY value:\"MyDatabase\""}
```
