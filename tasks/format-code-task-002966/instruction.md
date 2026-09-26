## Feature request: narrow down interactive results without enumerating everything to delete

When I run vgrep over a big tree I often get hundreds of matches, and the interactive shell is great for whittling them down — but `delete` is the only filtering tool, and it's awkward in the two cases I keep running into:

1. **Keeping a small subset.** Say I just want to focus on the matches inside one file. Since results are grouped per file, they form a contiguous index range like `42-57`. To end up with just those 16 lines I have to `delete 0-41` and then `delete 42-` (well, whatever the new upper bound is after the first delete). It's the opposite of what I actually want to say: "throw away everything except these".

2. **Filtering by a secondary pattern.** After the initial grep I often realise I want to further restrict the list to matches whose content also contains some substring/regex — e.g. I grepped for `foo` and now I only care about the ones that also mention `bar`. Today there is no way to do that inside the shell; I have to quit and re-run vgrep with a more complex pattern, losing my session.

Could the interactive shell grow two commands to cover these?

- One that's the inverse of `delete`: I give it a set of selectors and only those matches survive.
- One that takes a regex and drops every match whose content doesn't match it.

Both should behave like `delete` in that they modify the result list for the rest of the interactive session, and they should show up in the `?` help output alongside the other commands.

Naming-wise I'd expect something like `keep` (short `k`) for the first and `refine` (short `r`) for the second, mirroring how `delete`/`d` is invoked today.
