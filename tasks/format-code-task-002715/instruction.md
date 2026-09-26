## BigQuery: `function(...).* ` fails to parse

In BigQuery, when a function returns a `STRUCT`, you can splat all of its fields into the select list using `.*`, similar to how you can pick a single field with `.fieldname`. For example:

```sql
SELECT testFunction(a).*
FROM table1
```

This is valid BigQuery and runs fine in the actual warehouse, but sqlfluff (with `--dialect bigquery`) refuses to parse it — the `.*` after the function call comes back as unparsable.

Selecting a single named field off a function result (e.g. `testFunction(a).b`) does work, so it looks like only the wildcard form is missing. It would be great if the BigQuery dialect could accept `.*` in this position too.
