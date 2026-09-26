## `Override.sweep_string_iterator()` forces every sweep element to a string — hard to use from custom sweepers

I'm writing a sweeper plugin that wraps an external optimization library
(think Bayesian-optimization / TPE style). The library wants to consume
the candidate values in their native Python types — `float`, `int`,
`bool`, sometimes `list` / `dict` — so it can sample, compare and plot
them numerically.

The natural place to get the candidate list out of Hydra is `Override`.
Once the user types something like

```
lr=choice(0.001, 0.01, 0.1)
batch_size=range(8, 64, 8)
use_bn=true,false
```

I have an `Override` object and I want to enumerate the choices /
range and feed them to my optimizer.

The only enumeration API I can find on `Override` today is
`sweep_string_iterator()`, and it does what its name says: every element
comes out as a `str`. So I get `"0.001"` / `"0.01"` / `"0.1"` instead of
floats, `"8"` / `"16"` / ... instead of ints, `"true"` / `"false"`
instead of bools. I then have to write my own parser to turn them back
into the original types before handing them to the optimizer — and that
parser has to know how Hydra stringified each kind of value, which feels
like the wrong layer to be doing this work at. It also gets awkward for
list / dict elements, where round-tripping through a string is fragile.

What I'd really like is a way to enumerate sweep elements (at least for
the discrete sweeps — `CHOICE_SWEEP`, `SIMPLE_CHOICE_SWEEP`,
`GLOB_CHOICE_SWEEP`, `RANGE_SWEEP`) and get them back **as the native
parsed values**, not pre-stringified. Different sweepers will want
different things though:

- some want raw native values (my case)
- some want the current string form (whatever code is calling
  `sweep_string_iterator()` today)
- some sit in between — e.g. they're happy with primitives as-is but
  want complex values (lists, dicts, quoted strings) flattened to a
  string, because their backend can only key on hashable scalars.

So whatever the API ends up looking like, it would be great if the
caller could control how each element is presented on the way out,
rather than the iterator hard-coding one policy. And the existing
string-returning behavior obviously has to keep working — there's
already code depending on it.

Would it be possible to extend `Override` so sweeper plugins can get the
sweep elements out in a form they choose, instead of always going
through strings?

(I imagine the new entry point would be something like a `sweep_iterator(...)`
that takes a caller-provided transformer, with a small `Transformer` helper
exposing the three policies above — e.g. an `encode`-style one for the
hybrid case — but the exact naming is up to you.)
