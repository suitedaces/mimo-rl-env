# Align the bounds API with scipy

Right now `minimize` and `maximize` take box constraints through four separate
keyword arguments: `lower_bounds`, `upper_bounds`, `soft_lower_bounds` and
`soft_upper_bounds`. This is clumsy and does not match what people are used to
from `scipy.optimize`. We want a single, well-typed way to pass bounds.

## What to build

Introduce a public `Bounds` type, importable as `optimagic.Bounds`, that bundles
the four kinds of bounds into one object. It must be constructible with the
keyword arguments `lower`, `upper`, `soft_lower` and `soft_upper`, each of which
defaults to `None` and is readable back as an attribute of the same name. Like
the existing bound arguments, each field mirrors the structure of `params` (e.g.
an array for array params, a dict for dict params).

Add a new keyword argument `bounds` to both `minimize` and `maximize` that
accepts any of the following and applies the box constraints to the optimization:

- an `optimagic.Bounds` instance;
- a `scipy.optimize.Bounds` instance — its `lb`/`ub` become the lower/upper
  bounds (valid when `params` is a flat numpy array);
- a sequence of `(lower, upper)` pairs, one per parameter, as accepted by
  `scipy.optimize.minimize` (valid when `params` is a flat numpy array). Within a
  pair, `None` means that side is unbounded;
- `None`, meaning no bounds.

Anything else must raise `optimagic.exceptions.InvalidBoundsError`.

## Backwards compatibility

The old `lower_bounds`, `upper_bounds`, `soft_lower_bounds` and
`soft_upper_bounds` arguments must keep working exactly as before, but using any
of them must now emit a `FutureWarning` telling the user to switch to `bounds`.
When `bounds` is not provided, the values passed through the deprecated arguments
are used. When `bounds` is provided, it takes precedence over the deprecated
arguments (which, if also given, still trigger the warning).

The resulting optimization must respect the bounds regardless of which spelling
was used to provide them.
