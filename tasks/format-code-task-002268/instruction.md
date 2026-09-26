# Problem Statement

I'm trying to run some MySQL-compatible SQL that uses `SIGN(...)`, but TiDB doesn't recognize that function right now. Can you add support for `SIGN()` so I can get the sign of a numeric expression directly in queries?

# Expected outcomes

- `SIGN(expr)` can be used as a one-argument SQL function in TiDB queries.
- For numeric expressions greater than zero, `SIGN(expr)` returns `1`.
- For numeric expressions equal to zero, `SIGN(expr)` returns `0`.
- For numeric expressions less than zero, `SIGN(expr)` returns `-1`.
- `SIGN(NULL)` returns SQL `NULL`.
- Result metadata for `SIGN(expr)` reports an integer result type compatible with MySQL-style `BIGINT`/long long results.

# Implementation notes

The implementation should behave consistently with TiDB’s existing built-in SQL functions. The exact internal structure, helper functions, registration location, and validation path are left to the implementer.
