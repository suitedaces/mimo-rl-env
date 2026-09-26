IN operation doesn't parse with the clickhouse dialect
clickhouse:

```
albatross :) select 'a' in mapKeys(map('a', 1, 'b', 2));

SELECT 'a' IN mapKeys(map('a', 1, 'b', 2))

Query id: 29c42995-45a2-491c-8b36-cf0e51b2b39b

┌─in('a', mapKeys(map('a', 1, 'b', 2)))─┐
│                                     1 │
└───────────────────────────────────────┘

1 row in set. Elapsed: 0.001 sec.
```

sqlglot:

```
In [1]: import sqlglot as sg

In [2]: sg.parse_one("'a' IN mapKeys(map('a', 1, 'b', 2))", read="clickhouse")

...

File /nix/store/gi2hjdx10z60l2q3m5zld3y2v273fg2k-python3-3.10.6-env/lib/python3.10/site-packages/sqlglot/parser.py:563, in Parser.check_errors(self)
    561         logger.error(str(error))
    562 elif self.error_level == ErrorLevel.RAISE and self.errors:
--> 563     raise ParseError(concat_errors(self.errors, self.max_errors))

ParseError: Expecting (. Line 1, Col: 8.
  'a' IN mapKeys(map('a', 1, 'b', 2))

Expecting ). Line 1, Col: 35.
  'a' IN mapKeys(map('a', 1, 'b', 2))
```
