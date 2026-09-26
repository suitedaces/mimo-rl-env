## Missing ZMSCORE support

I'm using miniredis to unit-test a service that talks to Redis through go-redis. The service has a hot path where it needs to look up scores for a batch of members in a sorted set (a leaderboard), so instead of firing off N round-trips of ZSCORE it uses ZMSCORE to get them all in one call.

When I point the same code at miniredis in tests, the ZMSCORE call doesn't go through — miniredis doesn't seem to know about that command. ZSCORE works fine, so it looks like ZMSCORE just hasn't been wired up yet.

Could ZMSCORE be added? It's been a standard Redis sorted-set command for a while now and it'd be nice to be able to cover code paths that use it without having to rewrite them to loop over ZSCORE just for tests.

It would also be useful to have a matching Go helper on `Miniredis` / `RedisDB` alongside the existing `ZScore(...)`, so test setup/assertions can query multiple members at once directly without going through the protocol.
