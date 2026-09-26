I’m running multiple Agent instances with the same `REDIS_URL`, but keys using `ratelimit.type = "consistent"` still seem to be rate-limited separately per instance instead of sharing the Redis state. Can you make Redis actually back the consistent ratelimiter when `REDIS_URL` is set, with a clear startup log when it’s enabled and a fail-fast error if Redis can’t be used? Also, the cache dump keys in Redis are pretty generic as `dump:*`; it’d be nice if they were namespaced under cache dumps instead.

Expected outcomes:
- Consistent ratelimiting: when an Agent is configured with `REDIS_URL`, keys using `ratelimit.type = "consistent"` share ratelimit state across Agent instances that use the same Redis.
- Consistent ratelimiting: successful startup with Redis-backed consistent ratelimiting emits the log message `consistent ratelimiting enabled`.
- Startup failure: when `REDIS_URL` is configured but Redis-backed consistent ratelimiting cannot be used, the Agent fails fast and reports `unable to start redis ratelimiting`.
- Cache dump namespace: Redis cache dump and restore keys for key and API caches use the `cache:dump:*` namespace, specifically `cache:dump:keys:<machineId>` and `cache:dump:apis:<machineId>`.
- Cache dump namespace: the cache dump/restore logic no longer reads or writes the older generic `dump:*` cache dump keys.

Implementation notes:
- The exact data structures, initialization flow, and validation location are up to the implementation.
- Keep the behavior externally observable through the existing Agent configuration, startup logs, Redis state, and key verification behavior.
- Avoid changing unrelated rate limit modes or cache behavior outside the Redis-backed consistent ratelimit and cache dump key namespace described here.
