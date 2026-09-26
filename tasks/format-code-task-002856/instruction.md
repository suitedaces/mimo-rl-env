SQLGlot Fails if T-SQL FORMAT used with Culture Parameter
Repo:

```python
import sqlglot

sqlglot.parse_one("SELECT FORMAT(TimeStart, 'dddd', 'de-CH') FROM TableName", read="tsql")

```

Docs:  https://learn.microsoft.com/en-us/sql/t-sql/functions/format-transact-sql?view=sql-server-ver16 

The problematic line is to be found here: https://github.com/tobymao/sqlglot/blob/0746b6f96d9b8fad0d8fbea3e23170e8d56eb3ee/sqlglot/dialects/tsql.py#L82
