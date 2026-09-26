sort order is not rendered for duckdb
**Fully reproducible code snippet**

DuckDB has a setting `default_order`, which can be set to `'DESC'`, and results in unspecified sort order in `ORDER BY` queries being ordered according to `default_order`.

sqlglot seems to assume (reasonably so, I think) that `ORDER BY x ASC` is equivalent to `ORDER BY x`, which is an invalid assumption for duckdb given the presence of `default_order`:

```
In [4]: import sqlglot as sg

In [5]: sg.__version__
Out[5]: '18.5.1'

In [6]: sg.parse_one("select i from range(5) _ (i) order by i asc", read="duckdb").sql("duckdb")
Out[6]: 'SELECT i FROM RANGE(5) AS _(i) ORDER BY i'

In [7]: !duckdb
D set default_order = 'DESC';
D select i from range(5) _ (i) order by i;
┌───────┐
│   i   │
│ int64 │
├───────┤
│     4 │
│     3 │
│     2 │
│     1 │
│     0 │
└───────┘
```

**Official Documentation**

- https://duckdb.org/docs/sql/query_syntax/orderby.html
