# Problem Statement

I'm linting some SQL Server deployment scripts with SQLFluff, and right now the T-SQL partition setup statements just show up as unparsable. It'd be great if `sqlfluff parse --dialect tsql` could understand `CREATE/ALTER PARTITION FUNCTION` and `CREATE/ALTER PARTITION SCHEME` instead of choking on those DDL statements.

# Expected outcomes

- Partition functions: `sqlfluff parse --dialect tsql` parses SQL Server partition function creation statements as valid T-SQL statements, without treating the statement as unparsable, and exposes them as `create_partition_function_statement` in the parse output.
- Partition function changes: `sqlfluff parse --dialect tsql` parses SQL Server partition function alteration statements as valid T-SQL statements, without treating the statement as unparsable, and exposes them as `alter_partition_function_statement` in the parse output.
- Partition schemes: `sqlfluff parse --dialect tsql` parses SQL Server partition scheme creation statements as valid T-SQL statements, without treating the statement as unparsable, and exposes them as `create_partition_scheme_statement` in the parse output.
- Partition scheme changes: `sqlfluff parse --dialect tsql` parses SQL Server partition scheme alteration statements as valid T-SQL statements, without treating the statement as unparsable, and exposes them as `alter_partition_scheme_statement` in the parse output.
- Existing T-SQL parsing behavior outside these partition function and partition scheme statement forms should be preserved.

# Implementation notes

- Support this for the T-SQL dialect without changing behavior for other dialects.
- The exact grammar organization, helper structure, and validation location are up to the implementer as long as the observable parse behavior above is satisfied.
