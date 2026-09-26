# Problem Statement

I’m using the cross-repository issue/PR search API, but I can’t narrow the results to a specific owner or one of an org’s teams. It would be really helpful if I could search only within repos owned by a given user/org, and optionally within a team under that org, instead of getting everything I can see.

# Expected outcomes

- Owner-scoped issue/PR search:
  - `GET /repos/issues/search` supports an `owner` query parameter.
  - When `owner=<name>` is provided, results are restricted to issues and pull requests from repositories owned by the specified user or organization.
  - Existing search behavior continues to work when no `owner` parameter is provided.

- Team-scoped issue/PR search:
  - `GET /repos/issues/search` supports a `team` query parameter when an `owner` is also provided.
  - When `owner=<org>&team=<team>` is provided, results are further restricted to repositories associated with that team under the specified organization owner.
  - Supplying `team` without an `owner` returns HTTP 400 with error content indicating `Owner organisation is required for filtering on team`.

- Validation errors:
  - If `owner` names a user or organization that does not exist, the API returns HTTP 400 with error content indicating `Owner not found`.
  - If `team` names a team that does not exist under the specified owner, the API returns HTTP 400 with error content indicating `Team not found`.

- API documentation:
  - The Swagger/OpenAPI description for `GET /repos/issues/search` exposes an `owner` query parameter.
  - The Swagger/OpenAPI description for `GET /repos/issues/search` exposes a `team` query parameter, documented as requiring an organization owner parameter.

# Implementation notes

The implementation may choose where to parse, validate, and apply these filters, as long as the externally observable API behavior and documentation match the outcomes above. Preserve existing pagination, visibility, authentication, and other issue/PR search semantics except where the new owner/team filters intentionally narrow the search scope.
