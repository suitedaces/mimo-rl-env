Clickhouse: Ternary if parsing
Minimal code to reproduce:
```python
import sqlglot

sqlglot.parse_one(
    "flagcolumn ? created : now()",
    read="clickhouse"
)
```

While trying to parse expression with clickhouse ternary if, get the following error:
```
sqlglot.errors.ParseError: Invalid expression / Unexpected token. Line 1, Col: 28.
  flagcolumn ? created : now()
```

Documentation:
https://clickhouse.com/docs/en/sql-reference/functions/conditional-functions
