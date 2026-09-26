# Problem Statement

I’m seeing odd results from InfluxQL when I run arithmetic between two fields, like `SELECT a + b` or `a * b`: at timestamps where only one field has a value, the expression still returns a number, as if the missing field was treated as `0`. It happens with float fields, integer fields, and float/integer combinations, so I’m not sure if I’m misunderstanding how null field values are handled in binary expressions.

# Expected outcomes

- Float field arithmetic: for InfluxQL binary arithmetic expressions over two float fields, including addition, subtraction, multiplication, and division, any timestamp where either operand is missing/null should produce a null/missing expression result rather than a numeric result computed with an implicit zero.
- Integer field arithmetic: for InfluxQL binary arithmetic expressions over two integer fields, including addition, subtraction, multiplication, and division, any timestamp where either operand is missing/null should produce a null/missing expression result rather than a numeric result computed with an implicit zero.
- Mixed numeric field arithmetic: for InfluxQL binary arithmetic expressions combining float and integer fields in either operand order, including addition, subtraction, multiplication, and division, any timestamp where either operand is missing/null should produce a null/missing expression result rather than a numeric result computed with an implicit zero.
- When both operands are present at the same timestamp, existing arithmetic semantics should continue to apply for the supported numeric field type combination and operator.

# Implementation notes

- The fix should be expressed in terms of the observable InfluxQL query behavior above; the specific iterator structure, helper functions, data structures, and validation location are implementation choices.
- Preserve existing behavior outside binary arithmetic expressions over numeric field operands unless it is directly necessary to make missing/null operands propagate correctly.
