# Problem Statement

I’m trying to create a Kong route through the Admin API with a path like `/users:list` or `/items;v=2`, but the request gets rejected as `invalid path` with a “characters outside of the reserved list of RFC 3986 found” message.

# Expected outcomes

- Admin API route paths should allow RFC 3986 path-segment reserved characters when they are used in otherwise valid paths, rather than rejecting them solely as invalid path characters.
- Creating or updating routes with paths such as `/users:list`, `/items;v=2`, or other valid URI path-segment reserved-character usages should pass route path validation.
- Route paths that can use regex-style matching should still distinguish valid regex-style paths from syntactically invalid ones when these newly allowed URI characters are present.
- Malformed percent-encoding must remain invalid and should report an `invalid url-encoded value` validation error.

# Implementation notes

- The exact validation structure, helper functions, and where the checks are performed are implementation details.
- The fix should preserve existing path validation behavior for genuinely invalid path characters and malformed percent-encoding while allowing valid RFC 3986 path characters in route paths.
