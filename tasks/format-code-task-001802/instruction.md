# Fix the `mod` operator for negative operands

The `mod` operator in the standard library's arithmetic module gives mathematically
surprising answers whenever negative numbers are involved. For example, `-10 mod 3`
currently evaluates to `-1` and `10 mod -3` evaluates to `1`, which is the C-style
truncated-division remainder (its sign follows the left-hand operand).

That isn't what people expect from a modulo operation. `mod` should implement
*floored* modulo, i.e. the remainder of flooring division:

```
a mod b  ==  a - b * floor(a / b)
```

A direct consequence is that the result of `a mod b` always carries the **sign of
the divisor `b`** (or is exactly zero). Please make `mod` behave this way for both
integer and real operands.

Concretely, the operator must satisfy:

- `10 mod 3` is `1`
- `-10 mod 3` is `2`
- `10 mod -3` is `-2`
- `-10 mod -3` is `-1`
- `2 mod 5` is `2` and `-2 mod 5` is `3`
- `2 mod -5` is `-3` and `-2 mod -5` is `-2`
- when the result is `0` it stays `0` regardless of the signs of the operands
  (e.g. `9 mod 3`, `-7 mod 7`, `7 mod -7` are all `0`)
- real operands follow the same rule: `5.5 mod 2` is `1.5`, `-5.5 mod 2` is `0.5`,
  `5.5 mod -2` is `-0.5`, `-5.5 mod -2` is `-1.5`

Division by zero should keep its current behaviour; only the sign convention for
non-zero divisors needs to change.
