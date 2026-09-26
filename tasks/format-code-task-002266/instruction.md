## CASE WHEN expressions don't work

I tried to run a query with a `CASE WHEN` expression in the SELECT list and TiDB rejected it instead of evaluating the expression. Something like:

```sql
SELECT CASE WHEN c1 = 1 THEN 'one'
            WHEN c1 = 2 THEN 'two'
            ELSE 'other'
       END
FROM t;
```

and also the simple form:

```sql
SELECT CASE c1 WHEN 1 THEN 'one'
               WHEN 2 THEN 'two'
               ELSE 'other'
          END
FROM t;
```

Both fail — the planner refuses the statement instead of returning the values I'd expect. The same queries work fine in MySQL, so I'd expect TiDB to handle them the same way:

- evaluate the WHEN conditions in order and return the first matching THEN result
- if nothing matches and there's an ELSE, return that
- if nothing matches and there's no ELSE, return NULL
- a NULL condition is treated as "not matched" (skip and continue)

Could `CASE WHEN` get proper support in the expression handling so these queries actually run? Right now it looks like CASE just isn't wired up at all on the new path.
