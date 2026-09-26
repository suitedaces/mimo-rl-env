Unable to parse `KEEP QUOTES`/`OMIT QUOTES` in Trino
Found an [issue](https://github.com/apache/superset/issues/31768) when trying to parse a Trino query that uses `JSON_QUERY(col, jsonpath OMIT QUOTES)`:

```python
import sqlglot

# https://trino.io/docs/current/functions/json.html#id6
sql = """
SELECT
      id,
      json_query(description, 'strict $.comment' KEEP QUOTES) AS quoted_comment,
      json_query(description, 'strict $.comment' OMIT QUOTES) AS unquoted_comment
FROM customers
"""

sqlglot.parse_one(sql, read="trino")
```

Will raise:

```python
...
  File "/Users/beto/Projects/sqlglot/sqlglot/parser.py", line 5817, in _parse_function_call
    self._match_r_paren(this)
  File "/Users/beto/Projects/sqlglot/sqlglot/parser.py", line 7930, in _match_r_paren
    self.raise_error("Expecting )")
  File "/Users/beto/Projects/sqlglot/sqlglot/parser.py", line 1662, in raise_error
    raise error
sqlglot.errors.ParseError: Expecting ). Line 4, Col: 48.
```
