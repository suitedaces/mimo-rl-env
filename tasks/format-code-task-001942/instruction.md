I'm seeing duplicate entries piling up in my function's `external_invocation_urls`. It looks like the same API gateway URL shows up twice — once with a trailing slash and once without — even though it's really the same endpoint. The invoke URL I get back from the API gateway sometimes has that trailing `/` and sometimes doesn't, which I think is what's causing the mismatch.

Also, I've noticed it seems to be hitting the database even when I add a URL that's already there or remove one that isn't, which seems unnecessary. Could the URLs be normalized so the slash doesn't matter, and ideally skip the write when nothing actually changes?

Expected outcomes:
- API gateway invoke URLs returned through the public gateway schema/runtime surfaces should not differ only because one representation has a trailing slash.
- When a function external invocation URL is added through the existing add/update flow, trailing slashes should not cause duplicate entries for the same endpoint.
- Adding an external invocation URL that is already present should leave the function’s external invocation URL list unchanged and avoid a database write.
- Removing an external invocation URL that is not present should leave the function’s external invocation URL list unchanged and avoid a database write.

Implementation notes:
- URLs that differ only by trailing slash should be treated consistently across returned invoke URLs and stored function status.
- Preserve the existing behavior for genuinely new additions and genuinely existing removals.
- The exact validation location, data structure choices, and persistence-change detection mechanism are up to the implementation.
