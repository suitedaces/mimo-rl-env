## `Generator.random` silently accepts (or unhelpfully asserts) mismatched `out` arguments

When using `cunumeric.random.default_rng().random(...)` with an `out=` argument, the validation of `out` against `size` / `dtype` doesn't behave like a normal user-facing API.

Minimal repro:

```python
import numpy as np
import cunumeric as cn

rng = cn.random.default_rng(42)

# out dtype doesn't match the requested dtype
out = cn.empty((3, 3), dtype=np.float32)
rng.random(size=(3, 3), dtype=np.float64, out=out)

# out shape doesn't match size
out2 = cn.empty((3, 3), dtype=np.float64)
rng.random(size=(4, 4), dtype=np.float64, out=out2)
```

A couple of problems with the current behavior here:

1. The mismatch is checked with bare `assert` statements. That's not really
   the right tool for validating user-supplied arguments — Python run with
   `-O` strips asserts, so in optimized mode these calls go through silently
   and you end up with subtle wrong-shape / wrong-dtype results instead of
   an error.

2. Even when the assertion does fire, the user just gets a plain
   `AssertionError` with no message. There's no indication of which
   constraint failed or what the expected vs. actual values were, which
   makes this needlessly hard to debug — especially the dtype case, where
   the shapes might look fine and it's not obvious that the dtype is the
   problem.

I'd expect passing a mismatched `out` to raise a normal, descriptive
exception that's appropriate for the kind of mismatch (bad shape vs. bad
dtype), with a message that tells me what was expected and what I supplied,
and that this check stays in effect regardless of whether Python is run
with `-O`.
