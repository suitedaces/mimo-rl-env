## Analytics path normalisation doesn't recognise ULIDs

We use ULIDs as resource identifiers in our API paths, e.g.

```
/posts/01G9HHNKWGBHCQX7VG3JKSZ055/comments
/posts/01g9hhnkwgbhcqx7vg3jksz055/comments
```

Tyk's analytics path normalisation already handles UUIDs and numeric IDs nicely — when I enable `normalise_uuids` under `analytics_config.normalise_urls`, request paths containing UUIDs collapse to a single placeholder so the dashboard can aggregate hits per logical endpoint.

ULIDs aren't covered, though. Every request to the same logical endpoint shows up as a distinct path in analytics because the ULID segment is unique per resource, and there's no built-in option that catches them. The closest workaround is dropping a regex into `custom_patterns`, but ULIDs are a well-defined, widely used ID format (Crockford base32, 26 chars, case-insensitive) and it feels like they should be a first-class option alongside UUIDs rather than something every operator has to roll themselves.

Could Tyk gain built-in support for normalising ULIDs in analytics paths, in the same spirit as the existing UUID normalisation? Ideally it'd be off by default (so existing deployments don't change behaviour) and configurable from the same `normalise_urls` block.
