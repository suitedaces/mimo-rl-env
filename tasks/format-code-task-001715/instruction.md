## Feature request: overloads of `StringValuesBuilder.appendAll` accepting `Map` and `Pair` vararg

When building requests with Ktor I often end up with a `Map<String, String>` (or `Map<String, Iterable<String>>`) coming from config, query parsing, etc., and I want to dump the whole thing into `URLBuilder.parameters` or a headers builder in one line.

Today the only ways to bulk-append into a `StringValuesBuilder` are:

- `appendAll(stringValues: StringValues)` — requires me to first wrap my map into a `StringValues`
- `appendAll(name: String, values: Iterable<String>)` — one key at a time

So my code keeps looking like this:

```kotlin
val params: Map<String, String> = loadParams()

URLBuilder("https://example.com").apply {
    // I just want: parameters.appendAll(params)
    params.forEach { (k, v) -> parameters.append(k, v) }
}
```

Or for the multi-value case:

```kotlin
val multi: Map<String, List<String>> = mapOf(
    "tag" to listOf("a", "b", "c"),
)

URLBuilder("https://example.com").apply {
    multi.forEach { (k, vs) -> parameters.appendAll(k, vs) }
}
```

It would be a lot more ergonomic if `StringValuesBuilder` could just take a `Map` directly, and similarly accept loose `"k" to "v"` pairs without having to construct a `StringValues` first. Something like:

```kotlin
parameters.appendAll(mapOf("foo" to "bar", "baz" to "qux"))
parameters.appendAll(mapOf("tag" to listOf("a", "b", "c")))
parameters.appendAll("foo" to "bar", "baz" to "qux")
```

Both shapes of value should be supported:

- single-value entries (`Map<String, String>`, `Pair<String, String>`)
- multi-value entries (`Map<String, Iterable<String>>`, `Pair<String, Iterable<String>>`)

The behavior I'd expect is the same as if I had hand-written the `forEach { append(...) }` / `forEach { appendAll(...) }` loops above — i.e. it appends to (does not replace) any existing values for those keys, and it returns the builder so I can keep chaining.

Lives naturally in `ktor-utils` next to the existing `appendAll(StringValues)` extension in `StringValues.kt`.
