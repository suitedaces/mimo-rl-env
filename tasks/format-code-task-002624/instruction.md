## Feature request: ASCII-optimized case-insensitive comparison in the `ascii` package

I'm working on a hot path that does a lot of case-insensitive comparisons of short ASCII strings — think matching HTTP header names, JSON field keys, or protocol tokens against known constants (`"Content-Type"`, `"authorization"`, etc.). The standard library's `strings.EqualFold` / `bytes.EqualFold` work, but they're written to handle full Unicode case folding over UTF-8, which is way more than I need: in my case both sides are guaranteed to be plain ASCII.

When I profile, `EqualFold` shows up much higher than I'd expect for such a simple comparison, and it's because every byte goes through the general-purpose Unicode rune-decoding + folding path even though there's nothing non-ASCII to decode.

The `ascii` package in this repo already has nicely optimized `Valid` / `ValidString` helpers that take advantage of the ASCII-only assumption (with the AVX2 fast paths for longer inputs). It would be great to have a case-insensitive equality check in the same spirit — something I can call when I know both inputs are ASCII and want it to go as fast as possible. Both a `[]byte` form and a `string` form would be useful so I don't have to convert at the call site.

While we're on the subject, prefix/suffix variants (the case-insensitive equivalent of `bytes.HasPrefix` / `strings.HasSuffix`) would also be welcome — same motivation, I'm often checking whether a token starts/ends with a known ASCII keyword regardless of case.

Happy to help benchmark if useful.

For naming, I'd expect something along the lines of `EqualFold` / `HasPrefixFold` / `HasSuffixFold` for the `[]byte` versions, with parallel `...String` variants (`EqualFoldString`, etc.) for the `string` form, mirroring how the package already pairs `Valid` and `ValidString`.
