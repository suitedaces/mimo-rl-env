Support additional duckdb data types
I've started work to move our type parser in ibis from parsy to sqlglot for performance reasons: sqlglot is much much faster.

sqlglot is missing a few types that we previously supported (parsing metadata that come back from DuckDB's `DESCRIBE` directive) and while these aren't blocks because they are simple to intercept, it would be nice if sqlglot supported some or all of these.

**Is your feature request related to a problem? Please describe.**

Not related to a problem.

Here's the list of types that are currently supported by ibis and potentially returned from duckdb's `DESCRIBE` that aren't supported in sqlglot:

- `INT128`
- `HUGEINT`
- `NUMERIC` with no precision or scale arguments
- `TIMESTAMP_SEC`
- `TIMESTAMP_S`
- `TIMESTAMP_MS`
- `TIMESTAMP_US`
- `TIMESTAMP_NS`
- `TIMESTAMP_TZ`

**Describe the solution you'd like**

- `INT128`, `HUGEINT` -> `DataType.Type.INT128`
- `NUMERIC` -> `DECIMAL(18, 3)` DuckDB's default precision and scale
- `TIMESTAMP_*` -> ? not sure if these have an exact sqlglot equivalent

**Describe alternatives you've considered**

I've implemented the only viable alternative I can think of, which is to handle these strings before passing the text to sqlglot.

**Additional context**

NA
