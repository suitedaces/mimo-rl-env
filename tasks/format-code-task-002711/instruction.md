## Schema inference adds an extra dim for scalar features

I'm using `scio-tensorflow` to write out a batch of TF `Example`s along with an inferred schema. My examples have a mix of features — some are short arrays (a handful of floats per example), and some are scalars (one `int64` per example — things like a label, a timestamp, an id).

When I look at the resulting schema, the array features look fine, but the scalar features come back with a `FixedShape` that contains a single dim of size 1. So downstream TF code that reads this schema sees them as length-1 vectors rather than scalars — the dtype/values are right, but the shape doesn't match what those features actually are.

Repro is roughly:

```scala
// build some Examples where one feature is always exactly one value
// across every record, e.g. a label int64 + a couple of float arrays.
val examples: SCollection[Example] = ...

examples.saveAsTfExampleFileWithMetadata(path)
// or:
val schema = examples.inferExampleMetadata()
```

Then inspect the `Feature` entries in the produced `Schema`: the ones backed by a single value per Example come out with a non-empty shape (one dim of size 1) instead of the empty shape you'd expect for a scalar.

I'd expect scalar features to be represented as scalars in the inferred schema — no dim — while genuinely fixed-length array features (size > 1) keep their dim as today.
