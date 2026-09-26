BigQuery does not parse COUNTIF
Hello :wave:!   I noticed `COUNTIF` is not correctly transpiled from BigQuery to DuckDB, and while digging for the issue, it seems to be because it doesn't parse correctly.

In BigQuery it's `COUNTIF` [1] without underscore, but the default parser for this function seems to be `COUNT_IF`.

**Reproduction:**
```pyshell
λ python
Python 3.11.3 | packaged by conda-forge | (main, Apr  6 2023, 08:57:19) [GCC 11.3.0] on linux
[...]
>>> import sqlglot
>>> sqlglot.parse_one('select countif(x)', 'bigquery')
Select(
  expressions=[
    Anonymous(
      this=countif,
      expressions=[
        Column(
          this=Identifier(this=x, quoted=False))])])
```

I expected `countif` to be parsed as `exp.CountIf`, but it gets parsed as an anonymous expression.

I have a patch with a failing test case and a corresponding fix that I am happy to submit for review if that's of interest.

Thanks in advance.

Refs

[1] https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators
