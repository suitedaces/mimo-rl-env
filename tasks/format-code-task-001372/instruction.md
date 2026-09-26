# Embed pandas DataFrames into SQL templates

Our internal SQL templating helper (`bigframes.core.pyformat`) lets callers
splice values into a SQL string using Python `str.format`-style `{name}`
placeholders. Today it understands BigQuery table references, simple scalar
literals, and bigframes DataFrames, but if you hand it a plain pandas
`DataFrame` it rejects it with a `TypeError`. We want pandas DataFrames to be
first-class template values too.

The immediate motivation is *dry-run* query planning, where we want to validate
a query that refers to a local DataFrame **without** uploading any data and
**without** a started session. For that case we can embed the DataFrame as an
empty table expression that carries the right schema, which is enough for the
backend to plan the query.

## What to implement

`pyformat(...)` should gain two keyword-only options: a `dry_run` flag
(defaulting to off) and an optional `session`. These must be backward
compatible — existing callers that pass only the template and `pyformat_args`
keep working unchanged, and pandas DataFrames that aren't referenced by the
template are ignored.

When a referenced placeholder's value is a pandas `DataFrame`:

- **Dry run, no session available:** substitute an *empty table expression*
  with the DataFrame's schema, of the exact form

  ```
  UNNEST(ARRAY<STRUCT<...field list...>>[])
  ```

  where the field list contains one entry per column, in the DataFrame's column
  order, formatted as `` `column_name` TYPE ``. `TYPE` is the BigQuery type name
  the column's data would load as — e.g. `INTEGER`, `FLOAT`, `BOOLEAN`,
  `STRING`. A column holding lists/arrays is rendered as `ARRAY<TYPE>` of its
  element type, and a nested record/struct column as `STRUCT<...>`. Narrower
  numpy numeric types (such as `int32` or `float32`) are represented by their
  widened BigQuery type (`INTEGER`, `FLOAT`) rather than erroring out. Only the
  DataFrame's data columns participate; its index is not part of the schema.

- **No session and not a dry run:** embedding real DataFrame contents isn't
  possible without a session, so raise `ValueError`.

The substitution must be valid where a table would normally go (e.g. after
`FROM`), and unreferenced placeholders should never trigger validation or
embedding.
