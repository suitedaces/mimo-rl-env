## Exasol: `INTERVAL` literals don't parse

I'm linting some Exasol SQL with sqlfluff (`--dialect exasol`) and any
statement that uses an `INTERVAL` literal fails to parse. These are all
straight from the [Exasol docs on literals](https://docs.exasol.com/db/latest/sql_references/literals.htm),
so I'd expect them to be accepted.

A reduced repro — none of the following parse cleanly:

```sql
SELECT INTERVAL '5' MONTH;
SELECT INTERVAL '130' MONTH (3);
SELECT INTERVAL '27' YEAR;
SELECT INTERVAL '100-1' YEAR(3) TO MONTH;
SELECT INTERVAL '5' DAY;
SELECT INTERVAL '100' HOUR(3);
SELECT INTERVAL '1.99999' SECOND(2,2);
SELECT INTERVAL '23:10:59.123' HOUR(2) TO SECOND(3);
```

Running `sqlfluff parse --dialect exasol` on any of these gives unparsable
segments where the `INTERVAL ...` expression is.

It looks like the Exasol dialect just inherits the generic interval handling
which doesn't cover the shapes Exasol actually allows (precision in parens,
two-arg precision for `SECOND`, the various `… TO …` combinations, etc.).
Could the Exasol dialect support the full set of interval literals from the
docs above?
