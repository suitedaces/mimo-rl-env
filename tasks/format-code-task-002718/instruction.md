SQLFluff dbt templater requires Oracle dialect with 'AS' keyword for table alias
### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

SQLFluff dbt templater requires Oracle dialect with `as` keyword for table alias. When no `as` keyword is not found, it will produce `AL01` violation.

The problem is.. **Oracle does not support such keyword for table aliases**.

### Expected Behaviour

I'd expect to see no violations

```
==== no fixable linting violations found ====
All Finished 📜 🎉!
```

### Observed Behaviour

results in

```
== [/path/to/dbt_project/models/my_model.sql] FAIL
L:   4 | P:  29 | AL01 | Implicit/explicit aliasing of table.                                                                                                             
                       | [aliasing.table]
```

### How to reproduce

1. Create a valid Oracle dialect dbt project
2. Create a dbt model `my_model.sql`
    ```
    SELECT
        base.id,
        base.customer_id
    FROM {{ ref('customers') }} base
    ```
3. run `sqlfluff lint`

### Dialect

oracle

### Version

```
dbt-core==1.5.3
dbt-oracle==1.5.2
sqlfluff==2.1.4
sqlfluff-templater-dbt==2.1.4
```

### Configuration

```
[sqlfluff]
templater = dbt
dialect = oracle
sql_file_exts = .sql,.sql.j2,.dml,.ddl

[sqlfluff:templater:dbt]
project_dir = dbt_project/
profile = dbt_project
```

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
