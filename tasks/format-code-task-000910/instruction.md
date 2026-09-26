## Confusing overlap between `applyTo` and `reverseApply`

Two of the combinators shipped under `crocks/combinators` essentially do the
same thing — apply a value to a function — just with their arguments in the
opposite order:

- `applyTo :: (a -> b) -> a -> b` — function first, value second
- `reverseApply :: a -> (a -> b) -> b` — value first, function second
  (this is the Thrush)

This is awkward for a couple of reasons.

**The name `applyTo` doesn't really match what it does.** When I read
"apply X to Y" in English I expect "I have an X, here's the function Y, give
me Y(X)" — i.e. value first. So every time I reach for `applyTo` thinking
it's the Thrush, I find out it's the other order and have to go look up
`reverseApply` instead. The intuitive name and the actual A-combinator
behavior are mismatched.

**`reverseApply` is just an awkward name.** It's the bird that the rest of
the FP world calls Thrush, and it's the one I actually want most of the time
when working point-free. For example, in a typical `Reader` flow:

```javascript
const thrush = require('crocks/combinators/reverseApply')

Reader.of(57)
  .chain(x => ask(add).map(thrush(x)))
  .runWith(43)
```

I end up aliasing it to `thrush` locally just so the call site reads sensibly,
which is a hint that the export name isn't pulling its weight.

**And having both is redundant.** They're the same combinator with arguments
flipped; one of them can already be expressed in terms of the other plus
`flip`. Shipping both under the `combinators/` namespace gives users two
near-identical tools to choose between, and the docs have to describe the
distinction every time.

It would be nice to clean this up so there's one clearly-named combinator for
"apply a value to a function" (the Thrush) and stop exposing a second flipped
twin. I'm fine with this being a breaking change — happy to update call
sites — as long as what's left has a name that matches what it does.
