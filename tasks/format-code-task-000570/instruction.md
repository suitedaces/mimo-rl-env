## RangeIterator.Seek can return keys outside the requested range

I'm using bleve's KV store `RangeIterator(start, end)` and calling `Seek` on it to jump around within the range. I noticed that if I pass `Seek` a key that's lexicographically before `start`, the iterator happily positions itself there and starts yielding keys that are outside the range I asked for.

Minimal repro against the gtreap (in-memory) store — same thing happens with the boltdb store:

```go
// populate some keys: "a", "b", "c", "d", "e"
reader, _ := store.Reader()
it := reader.RangeIterator([]byte("c"), []byte("e"))

// seek to something before the range
it.Seek([]byte("a"))

for k, _, ok := it.Current(); ok; it.Next() {
    k, _, ok = it.Current()
    fmt.Printf("%s\n", k)
}
```

I expected the iterator to only ever yield keys in `[start, end)` regardless of what I pass to `Seek` — i.e. seeking to a key before `start` should behave the same as seeking to `start`. Instead I get `a`, `b`, `c`, `d` back.

This breaks the contract I'd expect from a range iterator: once I've constrained the iterator to `[start, end)`, no `Seek` should be able to escape that window on the low side. The high side (`end`) is already respected correctly.
