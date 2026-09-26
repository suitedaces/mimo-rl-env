## Problem Statement

When I list SCIM users or service principals through the Go APIs, the responses are huge because every item drags along all its roles, even though I usually don’t need them for filtering/listing. Can we avoid fetching roles for those list/filter calls by default, and give me a way to do the same for group filtering when I don’t need roles? I still need looking up a group by display name to give me the full group object, though.

## Expected outcomes

- User list and filter calls through the Go SCIM user API should request list results without per-user roles by default.
- Service principal list and filter calls through the Go SCIM service principal API should request list results without per-principal roles by default.
- The public Go group filtering API should let callers explicitly choose whether group list/filter results include roles. For this task, the public contract is `GroupsAPI.Filter(filter string, includeRoles bool) (GroupList, error)`.
- Calling `GroupsAPI.Filter` with `includeRoles` set to `false` should request group list/filter results without roles; calling it with `true` should preserve the previous behavior of requesting roles.
- Looking up a group by display name should still return the complete group object, including fields that are omitted from the initial list/filter lookup.

## Implementation notes

- Except for the public API contract explicitly named above, the exact internal structure, helper functions, and call sites are up to the implementation.
- Use the repository’s existing SCIM request patterns and error-handling conventions.
- Preserve existing filtering semantics apart from omitting roles where the behavior above requires it.

## Required output literals (exact-match contract)

When a SCIM user, service principal, or group list/filter request must omit roles, the outgoing SCIM request MUST include the query parameter `excludedAttributes=roles`. Query parameter order is not part of the contract.
