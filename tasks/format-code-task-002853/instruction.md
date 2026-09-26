Issue when calculating lineage when a CTE has the same name as a table from the schema
**Fully reproducible code snippet**

The following code 
```sql
from sqlglot.lineage import lineage

selected_column = "col_a"
sql = """
with 

my_cte_name_also_a_table_name as (
    select * from raw.schema.my_table
)

, inter as (
    select * from my_cte_name_also_a_table_name
)

select * from inter
"""

schema = {"raw": {"schema" : {"my_cte_name_also_a_table_name": {"col_1": "int"}, "my_table": {"col_a": "int"}}}}
schema_without_table = {"my_table": {"col_a": "int"}}

l = lineage(column=selected_column, sql=sql, schema=schema, dialect="snowflake")
```

returns the error
```
Traceback (most recent call last):
  File "/xxx/short_issue_lineage.py", line 21, in <module>
    l = lineage(column=selected_column, sql=sql, schema=schema, dialect="snowflake")
  File "/xxx/lib/python3.9/site-packages/sqlglot/lineage.py", line 148, in lineage
    return to_node(column if isinstance(column, str) else column.name, scope)
  File "/xxx/lib/python3.9/site-packages/sqlglot/lineage.py", line 136, in to_node
    to_node(
  File "/xxx/lib/python3.9/site-packages/sqlglot/lineage.py", line 112, in to_node
    source = optimize(
  File "/xxx/lib/python3.9/site-packages/sqlglot/optimizer/optimizer.py", line 89, in optimize
    expression = rule(expression, **rule_kwargs)
  File "/xxx/lib/python3.9/site-packages/sqlglot/optimizer/qualify_columns.py", line 49, in qualify_columns
    _qualify_columns(scope, resolver)
  File "/xxx/lib/python3.9/site-packages/sqlglot/optimizer/qualify_columns.py", line 250, in _qualify_columns
    raise OptimizeError(f"Unknown column: {column_name}")
sqlglot.errors.OptimizeError: Unknown column: col_a
```


It looks like there is an issue with the logic being confused between `my_cte_name_also_a_table_name` the CTE (with a column called `col_a`) and `my_cte_name_also_a_table_name` the table from the schema with a column called `col_1`.

With the example above, if I remove the table from the schema and calculate the lineage, the error goes away.
```
l = lineage(column=selected_column, sql=sql, schema=schema_without_table, dialect="snowflake")
```


Interestingly, the code without the intermediate cte `inter` calculates the lineage correctly when the table with the CTE name is provided in the schema.
```
sql = """
with 

my_cte_name_also_a_table_name as (
    select * from raw.schema.my_table
)

select * from my_cte_name_also_a_table_name
"""
l = lineage(column=selected_column, sql=sql, schema=schema, dialect="snowflake")
```
