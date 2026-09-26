# Problem Statement

When I call `GET /stamps`, I’m getting back old stamp entries whose batches don’t exist anymore, so the list is cluttered with unusable stuff. I’d rather have the normal response show only stamps that are still backed by an existing batch, and maybe have some explicit way to include the stale ones when I’m debugging.

# Expected outcomes

- Default stamp listing:
  - A `GET /stamps` response should include only stamps whose underlying batch still exists.
  - Stale stamp entries whose batch no longer exists should be omitted from the normal `stamps` array response.

- Explicit inclusion of stale entries:
  - `GET /stamps?all=true` should return all locally tracked stamps, including stale entries whose batch no longer exists.
  - Stale entries returned through the explicit “all” mode should still be represented as unavailable/non-existing in the existing response fields, such as `exists: false` and `usable: false`.

- Query parameter handling:
  - Only an `all` query value that is equal to `true` using case-insensitive comparison should enable the all-stamps response.
  - Missing `all`, `all=false`, or any other non-true value should use the default filtered behavior.

- API documentation:
  - The OpenAPI documentation for `GET /stamps` should document the optional `all` query parameter.
  - The route documentation should describe the endpoint as listing stamps without implying that the default response returns every tracked or every available batch.

# Implementation notes

- The exact data structures, helper functions, and validation location are implementation details.
- The behavior should be observable through the existing HTTP API and its documented response shape.
- Existing response fields for stamp availability should remain compatible with callers.
