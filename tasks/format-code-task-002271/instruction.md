## `UTC_TIME()` is not implemented

I'm porting an application from MySQL to TiDB and several of my queries use `UTC_TIME()` to grab the current UTC clock time (we log/compare timestamps across regions). On MySQL this just works:

```sql
mysql> SELECT UTC_TIME();
+------------+
| UTC_TIME() |
+------------+
| 14:32:07   |
+------------+
```

On TiDB the same query fails — the server tells me the function doesn't exist. Same thing if I try to pass a fractional-seconds precision argument like `SELECT UTC_TIME(6)`.

Since `UTC_TIME` is a pretty standard MySQL date-and-time builtin (documented at https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_utc-time), and TiDB already supports siblings like `UTC_TIMESTAMP()` and `CURRENT_TIME()`, it would be great to have `UTC_TIME()` actually work. It should:

- return the current UTC time when called with no arguments, and
- accept the optional fractional-seconds precision argument that MySQL allows.

Right now any query using it just blows up, which forces app-side workarounds for what should be a one-liner.
