### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

I use sqlfluff to lint my dbt project.

### Expected Behaviour

I assume there should be no error when using a templated region in the Where condition clause

### Observed Behaviour

When a Where condition clause is templated then an L007 error is raised.

### How to reproduce

Using the dbt templator and the included macro lint the following sql:

```SQL
{% macro binary_literal(expression) %}
  X'{{ expression }}'
{% endmacro %}

select
  *
from my_table
where
  a = {{ binary_literal("0000") }}
```

### Dialect

SparkSQL

### Version

```
sqlfluff: 0.12.0
Python 3.9.7
dbt  1.0.4
sqlfluff-templater-dbt : 0.12.0
```

### Configuration

```
[sqlfluff]
dialect = sparksql
templater = dbt

[sqlfluff:templater:dbt]
project_dir = ./

```

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
