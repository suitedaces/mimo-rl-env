Permission name discrepancy
When using this API endpoint to list permissions `http://localhost:8080/permissions/?APIToken=apitoken-demo` this is the list we get:

```
[
"access_system",
"manage_system",
"beacon_insert",
"query"
]
```

However, when adding a new role to Joola and using `query` in the permission list, we cannot query for results. Using `query:fetch` in the create role endpoint allows us to query Joola.
