## `jwk.Set` drops top-level fields other than `"keys"` when parsing

I'm consuming a JWKS document that, in addition to the `keys` array, has a few extra top-level fields that our auth team uses for bookkeeping. A trimmed example:

```json
{
  "issuer": "https://auth.example.com",
  "generated_at": "2021-11-20T08:00:00Z",
  "keys": [
    { "kty": "RSA", "kid": "k1", ... },
    { "kty": "RSA", "kid": "k2", ... }
  ]
}
```

When I parse this with `jwk.Parse` (or by `json.Unmarshal`-ing into a `jwk.NewSet()`), the keys come through fine, but I can't find any way to read `"issuer"` or `"generated_at"` off the resulting `jwk.Set`. There's nothing on the `Set` interface that exposes arbitrary top-level fields, and they aren't attached to the individual keys either (they don't belong to any single key — they're properties of the set as a whole).

To confirm they aren't just hidden somewhere, I also tried round-tripping:

```go
s, _ := jwk.Parse(data)
out, _ := json.Marshal(s)
fmt.Println(string(out))
// {"keys":[ ... ]}     // issuer / generated_at are gone
```

So the extra fields are silently dropped at parse time.

The JWK spec doesn't forbid additional members at the top level of a JWK Set, and in practice we (and I assume other people consuming third-party JWKS) do see them. It would be really useful if `jwk.Set` could:

1. preserve those extra top-level fields when unmarshaling, and
2. expose them through some accessor on `Set`, and
3. round-trip them back out when the set is marshaled to JSON again.

Right now we have to pre-parse the JSON ourselves to grab those fields before handing the bytes to `jwk.Parse`, which is awkward and means we're effectively parsing the JWKS twice.

The accessor I'd expect on `Set` is something like `Field(name) (value, ok)`, mirroring how `jwk.Key` already exposes its own extra fields.
