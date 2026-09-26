## `hash("md5")` is not supported in bloblang

I'm processing messages in a benthos pipeline and need to compute an MD5 of a field — we have a legacy downstream system that expects an MD5 checksum, and elsewhere I'd like to use short MD5-based keys for caching/deduplication.

In my mapping I wrote roughly:

```
root.checksum = this.content.hash("md5").encode("hex")
```

but the config fails to load because `md5` isn't a recognised algorithm for `hash`. Swapping it for `sha1` or `sha256` works fine, so the rest of the pipeline is OK — it's specifically that `md5` isn't an option.

Looking at the [bloblang docs for `hash`](https://www.benthos.dev/docs/guides/bloblang/methods/) the listed algorithms are only `hmac_sha1`, `hmac_sha256`, `hmac_sha512`, `sha1`, `sha256`, `sha512`, `xxhash64`. MD5 is obviously not appropriate for security-sensitive hashing, but for non-crypto use cases (checksums, cache keys, interop with existing MD5 data) it's still pretty common, and other connectors/tools tend to expose it.

Could `hash` learn an `"md5"` algorithm, with the same calling convention as the other algorithms (takes a string/bytes target, returns a byte array that can be passed through `encode("hex")` etc.)?
