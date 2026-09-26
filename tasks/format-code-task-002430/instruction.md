## Problem Statement

I’m seeing mypy report `Not enough arguments for format string` on old-style formatting like `"%d %d %d" % values` when `values` is typed as `Iterable[int]` or `Sequence[int]`, even though the same code runs fine when the iterable actually contains three items.

## Expected outcomes

- Old-style `%` formatting should not report `Not enough arguments for format string` solely because a non-tuple iterable-typed right operand has no statically known fixed length.
- Existing arity diagnostics should remain in cases where the right operand’s number of formatting arguments is still statically known.
- Other existing `%` formatting diagnostics should continue to behave as before outside this iterable arity edge case.

## Implementation notes

The exact implementation strategy, internal data structures, and validation location are up to the implementer. Keep the change focused on mypy’s externally visible diagnostics for old-style `%` string formatting.
