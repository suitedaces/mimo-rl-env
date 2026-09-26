Inconsistent formatting when leading_comma=True
Hi! This is something I noticed when trying out the [new formatting settings](https://github.com/TobikoData/sqlmesh/pull/2064) in SQLMesh, although I believe it's unrelated to that patch.  

```pycon
>>> import sqlglot
>>> print(sqlglot.__version__)
23.0.5
>>> sql = "select a, b, c from my_table"
>>> # first column has extra indentation
>>> print(sqlglot.parse_one(sql).sql(pretty=True, pad=4, indent=4, leading_comma=True))
SELECT
        a
    , b
    , c
FROM my_table
>>> # this is not the case when leading_comma=False
>>> print(sqlglot.parse_one(sql).sql(pretty=True, pad=4, indent=4, leading_comma=False))
SELECT
    a,
    b,
    c
FROM my_table
>>> # if pad=2, it formats consistently, but using 2 spaces rather than 4
>>> # (it also formats exactly the same with pad=2 and indent=2)
>>> print(sqlglot.parse_one(sql).sql(pretty=True, pad=2, indent=4, leading_comma=True))
SELECT
    a
  , b
  , c
```

There doesn't seem to be a combination of settings which 4-space-indents consistently with leading commas.
Am I misunderstanding something about how `pad` and `indent` interact?
