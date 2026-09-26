## ALTER TABLE ... ADD PARTITION does not work properly on a RANGE COLUMNS partitioned table

I have a table partitioned by `RANGE COLUMNS` (in my case on a `date` column, but the issue isn't specific to dates), e.g. roughly:

```sql
CREATE TABLE t (
    id   INT,
    d    DATE
) PARTITION BY RANGE COLUMNS(d) (
    PARTITION p0 VALUES LESS THAN ('2020-01-01'),
    PARTITION p1 VALUES LESS THAN ('2020-02-01')
);
```

The CREATE TABLE itself goes through fine. The problem is when I later try to add a new partition:

```sql
ALTER TABLE t ADD PARTITION (
    PARTITION p2 VALUES LESS THAN ('2020-03-01')
);
```

This does not behave the way I'd expect for a range-columns table. The validation that runs during ADD PARTITION seems to be the wrong one — it acts as if it's a `PARTITION BY RANGE (<expression>)` table where `LESS THAN` must be a plain integer, instead of a `RANGE COLUMNS` table where the bound is a tuple of column values (and the comparison should be based on the column types).

Symmetrically, I also tried adding a partition whose bound is clearly *not* strictly greater than the existing last partition, hoping it would be rejected the same way as for range-expression tables — but the rejection logic for range-columns partitions doesn't seem to be exercised on the ADD PARTITION path either.

So overall, on a `RANGE COLUMNS`-partitioned table, `ALTER TABLE ... ADD PARTITION`:

- can't add a perfectly valid new partition (it fails for the wrong reason), and
- doesn't correctly enforce the "strictly increasing bounds" rule for range-columns either.

I'd expect `ADD PARTITION` to be just as usable on `PARTITION BY RANGE COLUMNS(...)` tables as it is on `PARTITION BY RANGE (<expr>)` tables — same kind of value validation, same error semantics, just applied to the column-tuple form.
