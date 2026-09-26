Support alternative indentation of USING
Nice project. This is going to be really useful for us as we have a lot of BigQuery queries that other linters I've tried have struggled with.

However for JOINS, our preference is for this format:

```sql
SELECT
  a,
  b
FROM
  table1
JOIN
  table2
USING (a, b)
```

That is the `USING` is at the same indentation as the `JOIN`. To us it's another clause and so should be indented to the same level as the `SELECT`, `FROM`, and `JOIN`.

However sqlfluff doesn't like this so we need to disable L003, which is a shame as I'd like to have that enabled for other reasons.

Is there any possibility of either:
1. Adding an exception config to L003 to allow certain keywords (`USING` in our case, but probably also `ON`) to be automatically ignored, without adding a `-- noqa: L003` line to every instance of this or changing our preferred style?
2. Supporting this in a better way (so it would ideally actually check that `USING` is at the same level as `SELECT`, `FROM`, and `JOIN`).
