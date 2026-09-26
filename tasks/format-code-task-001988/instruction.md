## Allow regex patterns in `OIDC_EXEMPT_URLS`

I'm using `mozilla-django-oidc` on a Django site that has a bunch of XHR endpoints I'd like to keep out of `SessionRefresh`. XHR + session-refresh redirects is painful for client code, so I list those endpoints in `OIDC_EXEMPT_URLS`.

The problem is that some of those endpoints have variable segments in the URL path. For example I have routes like:

```
/signature/graphs/<field>/
/signature/aggregation/<aggregation>/
```

`<field>` and `<aggregation>` are arbitrary strings driven by the UI — not a fixed enum I can enumerate. So neither of the two options the setting currently supports really works for me:

- **Listing absolute paths**: I'd have to write down every concrete `<field>` value, which is unbounded.
- **Using Django view names**: I do have view names for these, but each view name resolves (via `reverse`) to a single concrete path, not the whole family of paths the URL pattern can produce. As soon as `<field>` is anything, `reverse` can't give me a useful exempt entry.

What I'd really like is to drop a compiled regex into the same list, e.g.

```python
import re

OIDC_EXEMPT_URLS = [
    "supersearch:search_fields",
    "/buginfo/bug",
    re.compile(r"^/signature/graphs/(?P<field>\w+)/$"),
    re.compile(r"^/signature/aggregation/(?P<aggregation>\w+)/$"),
]
```

…and have `SessionRefresh` treat any request whose path matches one of those patterns as exempt, alongside the existing string paths and view names. Today the middleware only compares `request.path` against the resolved string set, so the regex entries don't actually exempt anything — they just get treated as opaque values and never match.

Could `OIDC_EXEMPT_URLS` be extended to accept compiled regex patterns mixed in with the existing string entries?
