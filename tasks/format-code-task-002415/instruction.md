## `allows_any` / `allows_all` give wrong results for generic constraints

While playing with the generic constraints (`Constraint`, `MultiConstraint`, `UnionConstraint` from `poetry.core.constraints.generic`) I noticed that `allows_any` and `allows_all` don't agree with what the constraints actually represent as soon as you mix the different constraint kinds.

A few examples that surprised me:

```python
from poetry.core.constraints.generic import (
    Constraint, MultiConstraint, UnionConstraint,
)

eq_linux = Constraint("linux", "==")
ne_win   = Constraint("win32", "!=")
ne_linux = Constraint("linux", "!=")

# A MultiConstraint of negative constraints, e.g. != "win32" and != "linux"
multi = MultiConstraint(ne_win, ne_linux)

# A UnionConstraint, e.g. == "linux" or == "darwin"
union = UnionConstraint(eq_linux, Constraint("darwin", "=="))

# These come back with wrong values:
print(eq_linux.allows_all(multi))    # whether {linux} is a superset of (!=win32 and !=linux) -- obviously False
print(eq_linux.allows_any(multi))    # whether {linux} overlaps (!=win32 and !=linux) -- obviously False
print(ne_win.allows_all(union))      # whether (!=win32) is a superset of {linux, darwin} -- True
print(ne_win.allows_any(union))      # whether (!=win32) overlaps {linux, darwin} -- True
```

Several of these don't return what set theory says they should. The same kinds of inconsistencies show up when you flip the receiver and the argument (calling `allows_any` / `allows_all` on the `MultiConstraint` / `UnionConstraint` with a plain `Constraint`, or between two `MultiConstraint`s / `UnionConstraint`s).

It looks like the existing implementations only really handle a couple of the simple cases (constraint vs. constraint, or same kind vs. same kind) and silently fall through for the rest, so the answer ends up depending on which combination you happen to call.

I'd expect `c1.allows_all(c2)` to be true iff every value matched by `c2` is also matched by `c1`, and `c1.allows_any(c2)` to be true iff there's at least one value matched by both — regardless of whether `c1` / `c2` are `Constraint`, `MultiConstraint`, `UnionConstraint`, `AnyConstraint`, or `EmptyConstraint`.

Test coverage for these methods is also pretty thin right now, which is presumably how the wrong cases slipped through; it would be good to bring the coverage up alongside the fix.

### Side note on `Constraint.allows`

While I was at it I also got confused about what `Constraint.allows` is supposed to mean compared to `allows_any` / `allows_all`. For version constraints, `allows` takes a single concrete version, while `allows_any` / `allows_all` take arbitrary constraints. For generic constraints there's no separate "single value" type — the equivalent is a `Constraint` with the `==` operator. Right now `Constraint.allows` happily accepts `!=` constraints (and tries to interpret them), which doesn't really line up with the version-constraint contract and made it hard to tell which method I should be calling. It would be nice to make that interface less ambiguous.
