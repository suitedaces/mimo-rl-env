## Per-provider filtering for individual records

I'm using octodns to sync a zone to several DNS providers at once and I keep running into cases where I want a record to apply only to a subset of those providers — not every provider in my config.

The concrete case where this hurts: ALIAS records. Some of my providers support `ALIAS` natively (so I want them to receive the real ALIAS record), but at least one of my providers doesn't support `ALIAS` at all. For that provider I'd like to push a fallback `CNAME` on the same name instead.

Today both records have to live in the same yaml zone file, and there's no way to tell octodns which record is meant for which provider — so every provider tries to apply both, which either errors out (the provider that doesn't grok ALIAS) or produces a conflicting/duplicate state.

The existing flag I'd reach for is the per-record `octodns:` block with `ignored: true`, but that's an all-or-nothing switch — it hides the record from every provider, which isn't what I want. I want to keep the record, but only have it considered by some providers.

So what I'm looking for is a way, in the per-record `octodns:` metadata, to scope a record to specific provider(s) — either by listing the providers a record *should* be sent to, or by listing the ones it should be skipped for. That way the ALIAS-vs-CNAME case above becomes expressible: the ALIAS record is targeted at the providers that support it, and the CNAME fallback is targeted at the one that doesn't, all from a single yaml zone file.

`ignored` already covers the "drop everywhere" case, but it'd be really useful to have the more granular per-provider version for situations like this.

The two knobs I'd expect under the per-record `octodns:` block are something like `included: [...]` and `excluded: [...]` (lists of provider ids).
