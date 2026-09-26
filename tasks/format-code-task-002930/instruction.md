## Need a way to read all values of a repeated header

Some HTTP headers can legitimately appear multiple times in a single request/response — `Set-Cookie` on the response side is the obvious one, and on the request side things like `X-Forwarded-For`, `Via`, `Forwarded`, custom `X-...` headers, etc. are all routinely sent more than once.

With `RequestHeader` / `ResponseHeader` in fasthttp I can only see one of them. `Peek("X-Forwarded-For")` gives me a single `[]byte`, and `VisitAll` is the only way I've found to actually enumerate the duplicates — but that forces me to walk every header in the message and filter by key on every call, which is awkward when all I want is "give me every value for this one header name".

Minimal example of what I'd like to do:

```go
func handler(ctx *fasthttp.RequestCtx) {
    // request came in with multiple X-Forwarded-For headers
    values := ctx.Request.Header.???("X-Forwarded-For")
    for _, v := range values {
        log.Printf("xff hop: %s", v)
    }
}
```

and the same thing on the response side for collecting all `Set-Cookie` values from an upstream response.

`Args` already has `PeekMulti` / `PeekMultiBytes` for exactly this case on the query-args side, so it feels like the headers should have an equivalent. Could the request/response headers expose something similar that returns every value for a given header name?

A name like `PeekAll(key string) [][]byte` on both `RequestHeader` and `ResponseHeader` would feel natural here.
