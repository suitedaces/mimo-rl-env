# Problem Statement

When I call `Combine` with multiple path segments, I'm getting back several paths that have the exact same sequence of interfaces — they only differ in how they were assembled internally, but as far as routing goes they look identical to me. This clutters my results and I end up having to dedupe them myself. Could `Combine` just collapse paths with identical interface sequences down to a single one by default (ideally keeping whichever one stays valid the longest)? That said, occasionally I do want to see all the duplicates for debugging weird AS forwarding behavior, so it'd be nice if there were a way to opt back into getting all of them.

# Expected outcomes

- By default, `combinator.Combine` returns at most one path for each distinct sequence of path interfaces.
- If several combined paths have the same sequence of path interfaces, the default result keeps the representative whose metadata expires latest.
- `combinator.Combine` provides a caller-visible boolean opt-out for the default collapsing behavior.
- When that opt-out is enabled, `combinator.Combine` returns all matching combined paths, including multiple paths that share the same sequence of path interfaces but differ in their underlying segment construction.
- Existing callers that want the normal path list should use the default collapsing behavior.

# Implementation notes

- The concrete data structure, comparison mechanism, and validation location used to identify identical interface sequences are up to the implementer.
- The opt-out should be part of the public `Combine` API in a way that Go callers can use directly.
- The implementation should preserve existing path construction behavior except for the documented handling of identical interface sequences.
