## `ExpandFileContent` silently no-ops on `Substring`/`Regexp` with both `FileName` and `Content` set to true

I'm building search queries against zoekt and ran into a confusing edge case with `query.ExpandFileContent`.

My intent: I want a substring query that matches both filenames **and** file contents. Looking at `query.Substring`, there are two booleans `FileName` and `Content`, so the natural thing to do is set both to `true`:

```go
q := &query.Substring{
    Pattern:  "foo",
    FileName: true,
    Content:  true,
}
expanded := query.ExpandFileContent(q)
```

I expected `expanded` to be an `Or` of two atoms — one searching just filenames, one searching just contents — i.e. the same shape I'd get back from passing a `Substring` where neither flag is set.

What I actually get back is the original `Substring` unchanged, with both flags still `true`. Downstream that ends up being an atom claiming to be filename-only and content-only at the same time, which is not a meaningful state and gives me results I don't expect.

The same thing happens with `query.Regexp` — passing one in with `FileName: true, Content: true` comes back from `ExpandFileContent` untouched instead of being expanded into the two-branch `Or`.

It seems like "both flags true" should mean the same thing as "neither flag set" from `ExpandFileContent`'s point of view: in both cases the caller hasn't restricted to one side, so the query should be expanded into the OR of a filename-only branch and a content-only branch. Right now only the "neither set" case is handled and the "both set" case is silently ignored.

Could `ExpandFileContent` be fixed so that `Substring`/`Regexp` queries with `FileName == true && Content == true` are expanded the same way as ones with both flags false?
