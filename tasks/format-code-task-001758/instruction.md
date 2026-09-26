### Feature request: a reverse counterpart to `Str::wrap`

`Str::wrap()` lets you surround a value with a `before`/`after` string, which is handy. I keep running into the opposite need across projects and there's no clean helper for it.

A few examples of what I end up writing manually:

```php
// I want to strip the surrounding quotes off a value
$raw = '"Unquote"';
// expected result: Unquote

// I want to peel off the braces around a JSON-ish blob
$raw = '{ some: "json" }';
// expected result: ' some: "json" '
```

Today I have to hand-roll `substr` + `str_starts_with` / `str_ends_with` checks every time, and remember to only strip the delimiters when they're actually present (so I don't accidentally chop real content off a string that wasn't wrapped).

It would be great if `Str` (and the fluent `Stringable`) had a reverse of `wrap` that takes the same `(value, before, after = null)` shape as `Str::wrap` — symmetric with `wrap` so that wrapping and then unwrapping with the same arguments round-trips back to the original string, and where `after` defaults to `before` when omitted (same convention as `wrap`).

The new helper I'd expect is something like `Str::unwrap(...)` (with a matching method on `Stringable`).
