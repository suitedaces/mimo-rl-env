# Problem Statement

I'm trying to use `pingcap/parser` on SQL that contains `JSON_ARRAYAGG`, like `SELECT json_arrayagg(c2) FROM t GROUP BY c1`, but it fails during parsing even though TiDB/MySQL support that aggregate. Could you make the parser recognize it as an aggregate function, and also let Go callers refer to it through the usual `ast` aggregate-function constants instead of hardcoding the string?

# Expected outcomes

- SQL parsing:
  - Statements that call `JSON_ARRAYAGG` / `json_arrayagg` as an aggregate function parse successfully in the same contexts as other supported aggregate functions.
  - The parsed AST represents `JSON_ARRAYAGG(...)` as an aggregate-function call, with the aggregate name normalized consistently with the parser’s existing aggregate-function representation.
  - Invalid uses should continue to be rejected according to the parser’s existing aggregate-function validation rules.

- Go API:
  - The `ast` package exposes `AggFuncJsonArrayagg` as the aggregate-function name constant for `json_arrayagg`.
  - `ast.AggFuncJsonArrayagg` has the string value `"json_arrayagg"` so callers can compare against or construct aggregate-function AST nodes without hardcoding the literal.

# Implementation notes

Match the parser’s existing behavior for supported aggregate functions, including case-insensitive SQL recognition and AST normalization. The exact parser integration points, generated-code workflow, and internal token or grammar organization are left to the implementer.
