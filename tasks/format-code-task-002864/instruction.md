Unable to parse `WITH` / `WITHOUT` in Trino in JSON_QUERY
In the same vein as issue https://github.com/tobymao/sqlglot/issues/4623 we found [another issue](https://github.com/apache/superset/issues/31768) still in the JSON_QUERY using WITH and WITHOUT

```python
import sqlglot

# https://trino.io/docs/current/functions/json.html#json-query
sql = """he 
SELECT
      id,
      json_query(description, 'strict $.comment' WITH ARRAY WRAPPER) AS with_array,
      json_query(description, 'strict $.comment' WITHOUT ARRAY WRAPPER) AS without_array
FROM customers
"""

sqlglot.parse_one(sql, read="trino")
```

Will return an error:
```python
...
File [~/Project/dashboard-data/.venv/lib/python3.11/site-packages/sqlglot/parser.py:1602](https://file+.vscode-resource.vscode-cdn.net/Users/justin/Project/dashboard-data/~/Project/dashboard-data/.venv/lib/python3.11/site-packages/sqlglot/parser.py:1602), in Parser.raise_error(self, message, token)
   1590 error = ParseError.new(
   1591     f"{message}. Line {token.line}, Col: {token.col}.\n"
   1592     f"  {start_context}\033[4m{highlight}\033[0m{end_context}",
   (...)
   1598     end_context=end_context,
   1599 )
   1601 if self.error_level == ErrorLevel.IMMEDIATE:
-> 1602     raise error
   1604 self.errors.append(error)

ParseError: Expecting ). Line 4, Col: 48.
```

Version used: 26.3.9
