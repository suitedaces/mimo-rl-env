## Feature request: iterate over all entries in a cache

I'm using `otter.Cache[K, V]` and I'd like to be able to walk over every entry currently held in the cache (for example to dump the contents for debugging, export them somewhere, or compute some aggregate over the values).

Right now I can only ask the cache about a key I already know via `Get`/`Has`, or look at its `Size`. There doesn't seem to be any way to enumerate what's actually inside.

It would be great if `Cache` exposed an iteration API in the same spirit as `sync.Map.Range` — let the caller pass in a function that gets invoked for each entry, with the ability to stop iteration early when they've found what they were looking for. Expired entries shouldn't be surfaced through it (from the user's point of view those entries are already gone, even if they haven't been physically evicted yet).

Would you be open to adding something like this?
