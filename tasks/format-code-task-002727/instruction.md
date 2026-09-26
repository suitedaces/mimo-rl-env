Names of compound types of BigQuery are not recognized as type names
### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

I gave the following code to SQL Fluff:

```sql
create table foo (
    coord STRUCT<x INT64, y INT64>,
    items ARRAY<STRING>
)
```

### Expected Behaviour

I would expect no errors.

### Observed Behaviour

Instead I received 2 errors complaining about `STRUCT` and `ARRAY` being in uppercase.

- CP01 Keywords must be consistently lower case.

Why would I expect `STRUCT` and `ARRAY` to be treated as data type names, not as keywords:

- [BigQuery documentation](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data_type_list) lists ARRAY and STRUCT alongside all other normal data types like INT, STRING, DATE, etc.
- Other standard parametric data types of SQL like `VARCHAR(100)` aren't treated differently just because they take parameters.
- Other programming languages with parametric types don't usually have a different naming convention for the parametric v/s non-parametric types. For example `List<Date>` in Java.

This issue is loosely related to another type-names issue I created previously: #6792 

### How to reproduce

Just paste the above code to sqlfluff online.

### Dialect

BigQuery

### Version

3.3.1

### Configuration

None.

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
