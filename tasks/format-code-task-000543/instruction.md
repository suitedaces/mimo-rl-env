# Floor division and modulo for floats

VOC transpiles Python to Java by providing a runtime implementation of Python's
built-in types. Right now the `float` type is missing two arithmetic operators:
floor division (`//`) and modulo (`%`). Any program that uses them on a float
currently blows up instead of computing a result.

Please implement both operators on `float` so they behave exactly like CPython.

The left operand is a `float`; the right operand may be an `int`, a `float`, or a
`bool`. Concretely:

- `a // b` returns a `float` equal to the floor of the true division `a / b`
  (e.g. `9.9 // 2.0` is `4.0`, `-9.9 // 2.0` is `-5.0`).
- `a % b` returns a `float`. The result follows Python's convention that the
  modulo takes the **sign of the divisor**: `5.5 % -2` is `-0.5`, `-5.5 % 2` is
  `0.5`. When the remainder is exactly zero, the result is a signed zero whose
  sign matches the divisor, so `-7.0 % 7.0` is `0.0` while `7.0 % -7.0` and
  `0.0 % -3` are `-0.0`.
- A `bool` right operand acts like the integer `1` (`True`) or `0` (`False`).

Edge cases that must match CPython:

- Dividing or taking the modulo by a zero divisor (whether `0`, `0.0`, or
  `False`) raises `ZeroDivisionError`. Floor division by zero reports
  `float divmod()`; modulo by zero reports `float modulo`.
- Applying either operator with an unsupported right-hand type raises
  `TypeError` with the message
  `unsupported operand type(s) for //: 'float' and '<typename>'` (and the
  analogous message with `%` for modulo), where `<typename>` is the offending
  operand's type name.

Both the global scope and inside-a-function scope must produce identical results,
matching what CPython prints for the same source.
