# Safe composite resource-ID encoding/decoding

Throughout the provider, resources store a composite identifier by joining several
fields with the `#` separator (for example `apiKeyId#usagePlanId`) and later recover
the fields with a plain `strings.Split(id, "#")`. This breaks whenever one of the
fields itself contains a `#`: the split produces the wrong number of segments and the
resource can no longer find itself.

I'd like a small, reusable pair of functions in the provider package that make this
round-trip safe:

- `IdEncode(parts []string) string` — combine an ordered list of string fields into a
  single composite ID string.
- `IdDecode(id string) []string` — recover the original ordered list of fields from a
  composite ID string.

Required behavior:

- **Lossless round-trip.** For any non-empty slice `parts`, `IdDecode(IdEncode(parts))`
  must return a slice deep-equal to `parts` — same length, same order, same contents —
  no matter what characters the fields contain. In particular it must hold when a field
  contains the `#` separator, when a field is the empty string, and when several fields
  are empty. The number of recovered fields must equal the number of input fields.

- **Backward compatibility with the existing `#` format.** When every field is made up
  only of ordinary identifier characters (ASCII letters, digits, and `-`, `_`, `.`),
  `IdEncode` must produce exactly the fields joined by `#` — i.e.
  `IdEncode([]string{"a", "b", "c"})` is `"a#b#c"`. Symmetrically, a composite ID whose
  segments contain no `#` is decoded by splitting on `#`, so `IdDecode("a#b#c")` returns
  `[]string{"a", "b", "c"}`. This keeps already-stored identifiers stable and readable.

The two functions must be exact inverses of one another for any list of fields. Keep the
encoding deterministic (the same input always yields the same output).
