Hey, I'm using `SaveKeyValue` on the data trie tracker to store account data, and I just hit a node that basically blew up our storage because someone managed to stuff a single value that was several MB into one key. There's nothing stopping that right now — it just silently writes whatever you give it. Can we put some kind of cap on how big a single value can be so it refuses oversized writes instead of accepting them? And honestly it'd be nice if the call could actually tell me when it rejected something, since right now I have no way to know if the write went through.

Expected outcomes:
- Oversized value protection:
  - `DataTrieTracker.SaveKeyValue` / `TrackableDataTrie.SaveKeyValue` should reject a single value whose byte length is greater than the configured maximum leaf size.
  - Rejected writes should report a non-nil error that callers can recognize as the leaf-size-too-large condition, and the oversized value should not be recorded as pending account data.
- Accepted writes:
  - Values whose byte length is at or below the maximum leaf size should continue to be accepted and recorded normally.
  - Empty or nil values should continue to be valid inputs and should not be rejected by the size check.
- Error-aware API behavior:
  - `SaveKeyValue` should expose whether the write was accepted or rejected by returning an `error`.
  - Code paths that save account key/value data through `SaveKeyValue` should not silently continue after a rejected write; the error should be propagated or otherwise surfaced to the caller according to the surrounding API’s existing error-handling style.

Implementation notes:
- The exact validation location and internal organization are up to the implementer, as long as all public `SaveKeyValue` behavior is consistent.
- Use the project’s existing conventions for exported limits, reusable errors, and caller-side error propagation.
- Do not change the existing successful storage semantics for accepted values.
