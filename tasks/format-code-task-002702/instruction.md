## Problem Statement

I’m seeing `spacetime('February 30 2018')` get treated like a real date instead of being rejected as invalid. It looks like it ends up as a date in March, which is pretty surprising. Can you make `isValid()` catch impossible calendar dates like that?

## Expected outcomes

- Invalid calendar dates: Constructing a `spacetime(...)` value from an impossible calendar date, such as a day that does not exist in the parsed month/year, should not be silently accepted as a valid normalized date. Calling `.isValid()` on that value should report that the input is invalid.
- Valid calendar dates: Calendar dates that do exist, including valid leap-day dates, should continue to be accepted and should still return `true` from `.isValid()`.
- Public validity API: Callers should use `spacetime(...).isValid()` to observe validity. A `Spacetime` instance should not expose validity through a denormalized boolean `.valid` field.

## Implementation notes

The specific parsing checks, data structures, and validation flow are up to the implementation. Preserve the existing public construction and `.isValid()` usage patterns while making invalid calendar input observable through that public validity method.
