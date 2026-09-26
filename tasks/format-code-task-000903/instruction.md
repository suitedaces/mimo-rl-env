### `AncientRange` returns only one item when `maxBytes` is 0

I'm building a small tool that pulls items in bulk out of the freezer through the `ethdb.AncientReaderOp.AncientRange(kind, start, count, maxBytes)` API. In some code paths I genuinely don't care about a byte budget — I just want exactly `count` items if they're present in the freezer. The natural way to express "no byte limit" felt like passing `maxBytes = 0`, so I tried:

```go
items, err := db.AncientRange("bodies", start, 100, 0)
if err != nil {
    log.Fatal(err)
}
fmt.Println(len(items)) // expected: 100 (or however many are available)
```

What I actually get back is a slice of length 1. Asking for 50, 100 or 1000 items all behave the same — only the first one comes back. So in practice I have to call `AncientRange` in a loop one item at a time, which kind of defeats the point of having a range API.

The obvious workaround is to pass a huge number like `math.MaxUint64` for `maxBytes`, but that's awkward — it reads like "I'm fine allocating 16 EiB up front" rather than "I genuinely don't want a byte cap", and it also relies on the implementation not actually trying to honor that as a buffer size.

The current doc on `AncientRange` says it will return "at most `count` items, at least 1 item (even if exceeding maxBytes), but will otherwise return as many items as fit into maxBytes." That's a reasonable contract when the caller does specify a byte budget, but there's no documented way to say "no budget, just give me `count` items". It would be really useful if `maxBytes = 0` meant exactly that — return up to `count` items, ignoring any byte-size cap — while a nonzero `maxBytes` keeps behaving the way it does today.

This should apply both at the top-level `Freezer.AncientRange` and at the underlying `freezerTable.RetrieveItems`, since both take the same `maxBytes` parameter.
