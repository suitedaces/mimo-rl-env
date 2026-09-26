APPROX_COUNT_DISTINCT and ANY_VALUE
There are at least 2 (unrelated) functions that exist in BigQuery and have equivalents in ClickHouse: `ANY_VALUE()` is `any()` (note: exclusively lower case, `ANY` won't work) and `APPROX_COUNT_DISTINCT` is `uniq()` (note: same)

**Official Documentation**
- https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators#any_value
- https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators#approx_count_distinct
- https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/any
- https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/uniq#agg_function-uniq

Sqlglot completely ignores this:
```python
>>> sqlglot.transpile(
...     "SELECT APPROX_COUNT_DISTINCT(x) FROM (SELECT ANY_VALUE(y) x FROM (SELECT 1 y))",
...     read="bigquery",
...     write="clickhouse"
... )[0]
'SELECT APPROX_COUNT_DISTINCT(x) FROM (SELECT ANY_VALUE(y) AS x FROM (SELECT 1 AS y))'
```
(I've put the 2 in the same query, but those are 2 close but unrelated issues)

I'm pretty sure there are a ton of other things that are done differently, and not sure if the issue is in the parsing from bigquery dialect or dumping into clickhouse dialect (though I imagine it's the 2nd one).

What would be the best course of action ?
