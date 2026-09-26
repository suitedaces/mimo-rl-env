## Duplicate URLs being fetched when redirects are involved (`AllowURLRevisit=false`)

I'm using colly to crawl a site and I'm relying on the default behavior where the same URL shouldn't be fetched twice (I never called `AllowURLRevisit()`). Most of the time this works fine, but I've noticed two situations where the same page ends up being downloaded multiple times.

### Setup

A pretty standard collector:

```go
c := colly.NewCollector(
    colly.AllowedDomains("example.com"),
)

c.OnResponse(func(r *colly.Response) {
    fmt.Println("got:", r.Request.URL.String())
})

c.OnError(func(r *colly.Response, err error) {
    fmt.Println("error for", r.Request.URL.String(), ":", err)
})
```

I then call `c.Visit(...)` on a bunch of links I scraped from a listing page.

### Problem 1: redirects bypass the visited check

A lot of the URLs on the listing page are tracking/short links that 301/302 to the same canonical article URL. So I end up calling `Visit` on URLs like:

```
https://example.com/go?id=42
https://example.com/r/abc
https://example.com/articles/2024-01-15-hello
```

…and the first two redirect to the third. With `AllowURLRevisit=false` I expected each final page to be downloaded exactly once. Instead, in `OnResponse` I see the canonical URL printed three times, and the access log on my test server confirms `/articles/2024-01-15-hello` got requested three separate times.

If I `Visit` the canonical URL directly twice, the second call is correctly suppressed — so the de-dup logic itself works, it just doesn't seem to apply when the URL is reached via a redirect.

### Problem 2: trivial URL variations aren't deduped

Related, but probably the same root issue: URLs that differ only in something like a trailing slash are treated as completely different. So `Visit("https://example.com/foo")` followed by `Visit("https://example.com/foo/")` both go through to the server. From a crawling standpoint these are obviously the same resource and I'd expect the second one to be skipped.

### Expected

With the default `AllowURLRevisit=false`, once colly has actually fetched a given URL, subsequent attempts to fetch that same URL — whether passed directly to `Visit` or reached via a redirect chain — should be suppressed, and `OnError` should fire with something that clearly indicates "already visited" (ideally telling me *which* URL was the duplicate, since with redirects it isn't necessarily the one I passed to `Visit`).

Versions: latest `v2` from master.

I'd expect this to surface as a dedicated typed error (something like `*AlreadyVisitedError`) carrying the duplicate URL in a field (e.g. a `Destination *url.URL`), so callers can `errors.As` it and read off which URL actually got blocked.
