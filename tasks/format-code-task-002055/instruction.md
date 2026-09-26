# Add a urlscan.io reputation check for URLs found in e-mails

The analyzer already produces a set of `Verdict`s for an uploaded e-mail (SpamAssassin,
OleID, EmailRep, ...). We want a new verdict source that looks up the URLs extracted from
an e-mail's bodies against [urlscan.io](https://urlscan.io) and flags the ones that have
been scanned and judged malicious.

Add a urlscan verdict factory that mirrors the other verdict factories in the project: it
should be importable as `UrlscanVerdictFactory` from `app.factories.urlscan` and expose an
async classmethod

```python
verdict = await UrlscanVerdictFactory.from_urls(urls)   # urls: List[str]
```

that returns a `Verdict` (the project's existing verdict schema).

## How a URL is judged

For each URL, use the public urlscan.io API:

1. Query the **Search API** (`GET https://urlscan.io/api/v1/search/` with the query
   `q=task.url:"<url>"`) to find existing scans for that exact URL.
2. For every scan returned, fetch its **Result API** entry
   (`GET https://urlscan.io/api/v1/result/<uuid>/`) and read the overall verdict at
   `verdicts.overall` — a `malicious` boolean and an integer `score`.

A URL counts as malicious if any of its scans is flagged malicious. Outbound requests must
authenticate with the urlscan API key (taken from configuration, defaulting to empty) sent
as the `API-Key` request header.

## The resulting `Verdict`

- `name` is `"urlscan.io"`.
- When at least one URL is malicious: `malicious` is `True`, the overall `score` is `100`,
  and `details` contains exactly one entry per malicious URL. Each such detail has its
  `key` set to the URL, its `score` set to that scan's overall score, and a `description`
  that mentions the URL and a human-readable result link of the form
  `https://urlscan.io/result/<uuid>`.
- When no URL is malicious — including an empty URL list, URLs with no scans, or URLs whose
  scans are all benign — `malicious` is `False`, there is no overall `score` (it stays
  unset/`None`), and `details` holds a single entry noting that nothing suspicious was found.

## Robustness

Network or HTTP errors while looking up a particular URL (e.g. the Search or Result API
returns a non-2xx status) must be handled gracefully: that URL simply contributes nothing
to the verdict, and `from_urls` must never raise because of them. A new configuration value
for the urlscan API key should be available and default to empty when unset.
