### Description

The `kdoc-methods` rule reports individual missing-tag warnings on functions that don't have any KDoc at all.

If I have a public function with parameters (or a return type, or that throws something) but **no** `/** ... */` block above it, diktat reports both:

- `MISSING_KDOC_ON_FUNCTION` — fine, that's what I'd expect, and
- `KDOC_WITHOUT_PARAM_TAG` / `KDOC_WITHOUT_RETURN_TAG` / `KDOC_WITHOUT_THROWS_TAG` — which doesn't make sense, since there is no KDoc to be missing tags from.

### Reproducer

```kotlin
fun foo(a: Int, b: Int): Int {
    if (a < 0) throw IllegalStateException("negative")
    return a + b
}
```

(public, has params, has a non-Unit return, throws an exception, no KDoc at all.)

Running diktat on this file produces several warnings on the same function: one about the missing KDoc plus separate ones for each of `@param`, `@return`, `@throws`.

### Expected

When a function has no KDoc, only the "missing KDoc" warning should fire (and the autofix template should be generated as it already does). The "KDoc is missing a `@param`/`@return`/`@throws` tag" warnings should only apply when a KDoc block actually exists but is missing some tags — they're noise (and conceptually wrong) on a function that has no KDoc at all.
