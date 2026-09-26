## Redis cache: documents with hyphens / dots / colons in their id can't be queried

I'm running gorse with the Redis cache backend (redis-stack). My item ids are UUID-like strings such as `9b1c4f7a-2d3e-4a8b-bc12-7e5f0a1d9c33`, and some of my collection / subset names use dotted namespaces like `prod.recsys.v1`.

After `AddDocuments` succeeds, calling `SearchDocuments` / `UpdateDocuments` / `DeleteDocuments` against those documents doesn't behave correctly — the queries don't return the rows I just inserted, and update/delete end up being no-ops. The same code path works fine when the collection / subset / id are plain alphanumerics, so it really seems tied to those punctuation characters.

Minimal repro (roughly what I'm doing):

```go
ctx := context.Background()
collection := "prod.recsys.v1"
id := "9b1c4f7a-2d3e-4a8b-bc12-7e5f0a1d9c33"

_ = cache.AddDocuments(ctx, collection, "", []Document{{
    Id:         id,
    Score:      1.0,
    Categories: []string{"news"},
    Timestamp:  time.Now(),
}})

// expect to get the document back, but it's empty
docs, _ := cache.SearchDocuments(ctx, collection, "", []string{"news"}, 0, 10)
fmt.Println(len(docs)) // 0

// expect this to update the document I just inserted, but nothing changes
score := 2.0
_ = cache.UpdateDocuments(ctx, []string{collection}, id, DocumentPatch{Score: &score})
```

If I rename everything to use only letters/digits, the same flow works as expected. So the cache backend should support ids/collections/subsets that contain typical punctuation (UUID dashes, dotted namespaces, colon-separated keys) — these are pretty common in real-world data and the API doesn't document any such restriction.

Also, when something does go wrong inside the result-parsing path, the only error I get back is a generic `invalid FT.SEARCH result` with no detail, which makes it really hard to figure out which field tripped it up. It would help a lot if that error included what the offending value actually looked like.
