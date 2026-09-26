DuckDB dialect parse error: Quirks `LIMIT`
**Fully reproducible code snippet**
```python
from sqlglot import parse_one
sql='''SELECT 1 FROM ( SELECT 1 ) t( c ) WHERE ( ( VALUES(1), (c) LIMIT 1 ) INTERSECT ( SELECT 1 ) );'''
parse_one( sql, dialect = 'duckdb' )
```
```
Expecting ). Line 1, Col: 64.
  SELECT 1 FROM ( SELECT 1 ) t( c ) WHERE ( ( VALUES(1), (c) LIMIT 1 ) INTERSECT ( SELECT 1 ) );
```
**Official Documentation**
[LIMIT and OFFSET Clauses](https://duckdb.org/docs/stable/sql/query_syntax/limit)

**Package Version**
sqlglot 27.27.0
sqlglotrs 0.7.3
