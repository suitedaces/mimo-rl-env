# Add CookieJar serialization, deserialization, and cloning

Right now there's no supported way to persist a `CookieJar` and load it back later. We
need the ability to take a jar, turn it into a plain JSON-friendly structure, and
reconstruct an equivalent jar from that structure (or from its JSON string form). We also
want a convenient way to deep-copy a jar.

Please add the following to the public API.

## Serialization

Add an instance method `serialize(cb)` (asynchronous, node-style `cb(err, serialized)`) and
its synchronous counterpart `serializeSync()` that returns the serialized object directly.
`toJSON()` should be an alias that returns the same structure, so `JSON.stringify(jar)`
works.

The serialized value is a plain object with these fields:

- `version` — the string `"tough-cookie@"` followed by this package's version (from
  `package.json`).
- `storeType` — the name of the jar's store type (for the built-in in-memory store this is
  `"MemoryCookieStore"`).
- `rejectPublicSuffixes` — a boolean reflecting the jar's configuration.
- `cookies` — an array with one entry per cookie currently held by the jar. Each entry is a
  **plain object** (not a live cookie instance) carrying the cookie's data, suitable for
  `JSON.stringify`. Any date-valued fields are rendered as ISO-8601 strings, and internal
  sorting/bookkeeping fields are not exposed.

The whole structure must survive `JSON.stringify` / `JSON.parse` without losing cookie
data.

## Deserialization

Add static methods `CookieJar.deserialize(serialized, [store,] cb)` (asynchronous) and
`CookieJar.deserializeSync(serialized, [store])` that build a `CookieJar` from a serialized
value. The `serialized` argument may be either the object produced by `serialize` **or** its
JSON string form. The optional `store` argument lets the caller supply a destination store;
when omitted, a fresh in-memory store is used. The reconstructed jar must carry over the
`rejectPublicSuffixes` setting. `CookieJar.fromJSON(serialized)` is a synchronous alias of
`deserializeSync`.

Round-tripping must be faithful: for any request URL, the jar produced by deserializing must
return exactly the same cookies — same values and same ordering — as the original jar would
have. In particular, cookie creation timestamps must be preserved so that the relative
ordering of cookies is unchanged after a serialize/deserialize cycle.

## Cloning

Add an instance method `clone([store,] cb)` (asynchronous) and `cloneSync([store])` that
produce an independent deep copy of the jar. The copy must be fully decoupled from the
original: adding or changing cookies in one jar must not affect the other.

The bundled in-memory store should support being serialized this way (i.e. it must be able
to enumerate all the cookies it holds).
