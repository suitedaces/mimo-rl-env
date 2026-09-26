I’m using `faker.number.float` for test data and I need the generated numbers to stay within a fixed number of decimal places; right now I’m having to work around it with rounding or `multipleOf`, which feels indirect. Could it have a simple way to say how many fraction digits are allowed so the floats don’t come back with long decimal tails?

Expected outcomes:
- `faker.number.float` supports a `fractionDigits` option for limiting generated floating-point values to at most the requested number of digits after the decimal point.
- Generated values using `faker.number.float({ fractionDigits: n })` still respect the usual numeric range options such as `min` and `max`.
- `fractionDigits` must be a non-negative integer.
- Passing both `multipleOf` and `fractionDigits` to `faker.number.float` is invalid and throws a `FakerError` with the message `multipleOf and fractionDigits cannot be set at the same time.`
- Passing a non-integer `fractionDigits` throws a `FakerError` with the message `fractionDigits should be an integer.`
- Passing a negative `fractionDigits` throws a `FakerError` with the message `fractionDigits should be greater than or equal to 0.`

Implementation notes:
- The concrete validation location and internal representation are up to the implementation.
- Existing supported behavior for `faker.number.float`, including `multipleOf`, deprecated precision handling, and min/max validation, should remain compatible unless explicitly covered by the new `fractionDigits` rules above.
