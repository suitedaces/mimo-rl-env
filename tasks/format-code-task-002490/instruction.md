# Reusable RQL → SQL query-building helpers

We're adding RQL-driven listing (filtering, full-text search, pagination and grouping) to several
admin list endpoints, starting with prospects. Rather than hand-roll the SQL in every repository,
we want a small set of **reusable, composable helpers** that take an already-parsed RQL query plus a
`goqu` select dataset and return the dataset with the relevant clauses applied. They will be reused
across resources, so the behavior needs to be well-defined and not specific to any one table.

Add these to the project's shared utilities package (`github.com/raystack/frontier/pkg/utils`). They
build on `github.com/doug-martin/goqu/v9` and the parsed-query types in
`github.com/raystack/salt/rql` (`rql.Query`, `rql.Filter`). Each helper receives a
`*goqu.SelectDataset` and returns a `*goqu.SelectDataset` so callers can chain them.

The generated SQL is exercised against PostgreSQL (`goqu.Dialect("postgres")`).

## Result metadata types

Expose value types the callers can return to clients:

- `Page` with integer `Limit` and `Offset` fields and an `int64` `TotalCount` field.
- `Group` with a `Name string` and a `Data []GroupData`.
- `GroupData` with a `Name string` and an `int` `Count`.

## Pagination

`AddRQLPaginationInQuery(query *goqu.SelectDataset, q *rql.Query) (*goqu.SelectDataset, Page)`

Applies `LIMIT` and `OFFSET` to the query and reports what was applied via the returned `Page`
(`TotalCount` is left for the caller to fill in):

- When the requested limit is not a positive number, fall back to a default limit of **50**.
  Otherwise use the requested limit.
- When the requested offset is not positive, fall back to **0**. Otherwise use the requested offset.
- The returned `Page.Limit` / `Page.Offset` must reflect the values actually applied to the query.

## Filters

`AddRQLFiltersInQuery(query *goqu.SelectDataset, q *rql.Query, supportedColumns []string, checkStruct interface{}) (*goqu.SelectDataset, error)`

Adds one `WHERE` condition per requested filter, AND-ed together (every filter must hold):

- If a filter targets a column that is not present in `supportedColumns`, return a non-nil error and
  do not run the query.
- The data type of each filter's column is taken from the `rql` struct tags on `checkStruct` (use the
  `rql` package to resolve it). The condition is built according to that data type and the filter's
  operator and value.
- Standard comparison operators (`eq`, `neq`, `gt`, `lt`, `gte`, `lte`) produce the corresponding SQL
  comparison against the column for numeric, boolean, datetime and string columns.
- For string columns, the membership operators `in` / `notin` treat the value as a comma-separated
  list: `"a,b,c"` must match/exclude each of `a`, `b`, `c` as separate values (not a single literal).
- For string columns, `like` / `notlike` perform a **case-insensitive** partial match (and its
  negation) against the column.

## Search

`AddRQLSearchInQuery(query *goqu.SelectDataset, q *rql.Query, searchableColumns []string) (*goqu.SelectDataset, error)`

Applies a single free-text search across columns:

- When the search term is empty, leave the query unchanged.
- Otherwise add a condition that matches when **any** of `searchableColumns` contains the search term
  as a **case-insensitive** substring (the per-column matches are OR-ed together).

## Grouping

`AddGroupInQuery(query *goqu.SelectDataset, q *rql.Query, allowedColumns []string) (*goqu.SelectDataset, error)`

Turns the query into a grouped aggregation that yields each distinct group value alongside its row
count:

- When no group-by columns are requested, leave the query unchanged (no `GROUP BY`).
- If any requested group-by column is not in `allowedColumns`, return a non-nil error.
- Otherwise select the grouped value plus a `COUNT` of the rows in each group and `GROUP BY` the
  requested column(s). A single group column is grouped/selected as-is; when two columns are
  requested the group value is the two columns joined by a comma separator.
