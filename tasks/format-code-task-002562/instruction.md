`dig.SPF` returns an empty (or near-empty) list for most real domains

I'm trying to use the `dig` execution module to pull the list of IPs a domain authorizes for sending mail, so I can sync them into firewall rules. Most of the domains I care about come back essentially empty.

For example:

```
# salt ns1 dig.SPF google.com
ns1:
    []
```

But google.com obviously *does* publish an SPF policy — `dig +short google.com TXT` shows it, it's just that the record is mostly composed of `include:_spf.google.com` (which itself includes more sub-records) rather than listing `ip4:` ranges inline. Same story for most providers I checked: the top-level SPF record delegates via `include:` (or sometimes `redirect=`) and `dig.SPF` doesn't follow any of that, so the caller is left with nothing usable.

A couple of related things I noticed while poking at this:

- Domains that publish IPv6 ranges via `ip6:` mechanisms also don't show up in the result — only `ip4:` ones seem to be considered at all. For a function whose job is "give me the IPs this SPF record authorizes" that feels incomplete.
- Tangentially: every other execution module I use day-to-day exposes its functions with lowercase names (`pkg.install`, `service.start`, …), but `dig` only accepts the uppercase forms — `salt ns1 dig.spf google.com` errors out and I have to remember to type `dig.SPF`. Minor papercut but it's the only module I have to special-case in my muscle memory.

What I'd expect from `dig.SPF <domain>` is: chase the record all the way down (through includes / redirects) and hand me back the full flat list of IP ranges the domain ultimately authorizes, v4 and v6.
