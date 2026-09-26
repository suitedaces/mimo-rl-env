### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

ASOF join syntax was [recently added in Snowflake](https://docs.snowflake.com/en/sql-reference/constructs/asof-join) and is not currently supported in SQLFluff. This is similar to issue [5536](https://github.com/sqlfluff/sqlfluff/issues/5536) to add ASOF joins to DuckDB.

### Expected Behaviour

ASOF joins should parse as a join_clause.

### Observed Behaviour

When using an ASOF join, SQLFluff returns:

> Implicit/explicit aliasing of table.sqlfluff(AL01)
Alias 'ASOF' is never used in SELECT statement.sqlfluff(AL05)
Unquoted identifiers must be lower case.sqlfluff(CP02)

Also, columns referenced from tables after the ASOF statement give the following:

> Reference '{table}.{column}' refers to table/view not found in the FROM clause or found in ancestor statement.sqlfluff(RF01)

### How to reproduce

```
SELECT t.stock_symbol, t.trade_time, t.quantity, q.quote_time, q.price
FROM trades t
  ASOF JOIN quotes q
    MATCH_CONDITION(t.trade_time >= quote_time)
    ON t.stock_symbol=q.stock_symbol
ORDER BY t.stock_symbol;
```

### Dialect

Snowflake

### Version

3.0.2

### Configuration

defaults

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
