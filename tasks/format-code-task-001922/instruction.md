## `rotateLeft` / `rotateRight` don't work when called with a `Nat` value

`HListOps` and `TupleOps` both expose a `rotateLeft` / `rotateRight` that's supposed to mirror the style of `take`, `drop`, `apply`, `split`, ... — i.e. you can call it either with an explicit type argument or by passing a `Nat` value. The value-argument form is broken.

For example, the following compiles and behaves correctly:

```scala
import shapeless._
import syntax.std.tuple._

(1, 2, 3, 4, 5).take(Nat._2)   // ok, gives (1, 2)
```

but the analogous call to `rotateLeft` / `rotateRight` doesn't:

```scala
(1, 2, 3, 4, 5).rotateLeft(Nat._2)    // doesn't work
(1, 2, 3, 4, 5).rotateRight(Nat._2)   // doesn't work
```

Same story for the `HList` syntax — `hlist.rotateLeft(Nat._2)` doesn't work the way `hlist.take(Nat._2)` does.

The explicit-type-argument form (`rotateLeft[_2]`) is the one I usually see in examples, but it'd be nice if the value form worked too — every other "by-N" operation in `HListOps` / `TupleOps` supports both styles, so `rotateLeft` / `rotateRight` look like an oversight.
