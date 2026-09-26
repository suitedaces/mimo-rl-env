### Pyright doesn't flag re-declaration of fields when subclassing a `NamedTuple`

I have a small class hierarchy where the base class is a `typing.NamedTuple`, and a subclass re-declares one of the parent's fields:

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class ColoredPoint(Point):
    x: float          # re-declaring the field from Point
    color: str = "red"
```

Pyright doesn't say anything about the `x: float` line, even with `reportIncompatibleVariableOverride` enabled.

I'd expect this to be flagged. NamedTuple fields are read-only at runtime — the subclass can't actually replace `x` in the underlying tuple slots, so a re-declaration like this is at best dead noise and at worst quietly misleading (e.g. it makes it look like `ColoredPoint(...).x` is now a `float`, but the value still comes from the tuple element the parent set up).

Other type checkers I've tried do warn on this. It would be great if pyright caught it too — re-declaring a field inherited from a `NamedTuple` parent should produce a diagnostic in the same family as the existing variable-override checks, so I can opt into seeing it via the usual incompatible-override settings.
