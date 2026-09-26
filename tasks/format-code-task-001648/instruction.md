# Fix `pyfloat` when only one bound is supplied

`Faker().pyfloat(...)` (in the Python provider) is broken in a few ways once you
combine `min_value`/`max_value` with `left_digits`/`right_digits`. The generator
should always be able to produce a valid float that simultaneously respects every
constraint it was given, but today it crashes or ignores the bound in several
common cases.

## What needs to work

**One-sided bounds combined with digit limits.** When exactly one of `min_value`
or `max_value` is provided (the other left as `None`) together with explicit
`left_digits` and `right_digits`, the call must reliably return a `float` that:

- respects the supplied bound — `result >= min_value` when only `min_value` is
  given, `result <= max_value` when only `max_value` is given (works for positive
  and negative bounds alike);
- has no more than `left_digits` digits in its integer part and no more than
  `right_digits` digits in its fractional part;
- never raises — repeated calls with the same arguments must all succeed instead
  of intermittently throwing `TypeError` (or any other exception).

For example, `pyfloat(min_value=99884.7, max_value=None, left_digits=5, right_digits=2)`
and `pyfloat(min_value=None, max_value=11000.3, left_digits=5, right_digits=2)`
must both keep producing in-range numbers no matter how many times they are called.

**Large-magnitude bounds.** A bound that is large in magnitude but still
representable within Python's float significant-digit limit must be honoured
rather than blowing up with an internal "empty range" error. For instance,
`pyfloat(max_value=100000000000001.0)` and `pyfloat(max_value=-1000000000000001.0)`
should return a float that is `<= max_value`.

**Out-of-range bounds.** A bound whose magnitude is too large to be represented
within the float significant-digit limit (e.g. a `min_value`/`max_value` with far
more digits than `sys.float_info.dig` allows) must raise `ValueError`.

All existing behaviour and validation of `pyfloat` must be preserved.
