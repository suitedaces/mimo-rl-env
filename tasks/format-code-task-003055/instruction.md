## Missing type class instances for `Unit`

I'm using zio-prelude in some generic code that occasionally needs to combine values of `Unit` type (for example, a tuple like `(String, Unit)` where one slot is a placeholder, or directly using `<>` on `Unit` values inside a more polymorphic helper).

I expected this to "just work" because every other basic type seems to have the relevant type class instances available out of the box — `Boolean`, `Byte`, `BigInt`, `BigDecimal`, etc. all have things like `Commutative`, `Identity`, `Inverse` defined for them. So calling `<>` on those, or summoning an `Identity` for tuples that include them, compiles fine.

But the moment `Unit` shows up, the implicit search fails and my code stops compiling. Since `Unit` only has one inhabitant (`()`), it's arguably the most trivial case there is — combining `()` with `()` is obviously still `()`, and `()` is obviously the identity — so it's surprising that this isn't already provided alongside the other primitives.

Could the standard set of instances for `Unit` be added so it's consistent with the rest of the basic types?
