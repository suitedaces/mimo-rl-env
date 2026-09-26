## `Fido.search` with `Instrument.soon` returns bogus results for dates NOAA doesn't actually cover

I'm using sunpy to pull NOAA SWPC Solar Region Summary data across a long time span — something like the past few solar cycles — so I do:

```python
from sunpy.net import Fido, attrs as a

results = Fido.search(a.Time("1980-01-01", "2016-01-02"),
                      a.Instrument.soon)
print(results)
```

The search returns a result row for every day in the range, which initially looked great. But when I then try `Fido.fetch(results)`, a huge chunk of the downloads fail — the URLs for the early years just don't exist on the SWPC FTP server. Looking at the URLs that come back from `search`, the client is happily constructing ftp paths for years that NOAA simply doesn't have parseable SRS data for (the very old years aren't in the same format the client expects).

I'd expect `search` itself to know what NOAA actually has and only hand me back rows for dates where there's real data — not give me a wall of records that are guaranteed to fail at fetch time. If I query a range that's entirely outside what NOAA provides, I'd expect zero results rather than a pile of dead links.

Same thing on the other end of the range: if I accidentally set the end time past today (e.g. a script that does `Time.now() + something`), I get rows for future dates too, which obviously can't be real either.

Could `SRSClient` filter its search results down to the dates that NOAA actually serves?
