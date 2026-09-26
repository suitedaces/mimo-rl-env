## Problem Statement

I’m hitting a weird issue through the Vault Agent caching listener: when Vault rejects a request, the client just gets a 500 with `failed to get the response:` instead of the Vault error I see when calling Vault directly, like a 403 permission denied or a 404.

## Expected outcomes

- Requests sent through the Vault Agent caching listener should preserve Vault rejection responses when Vault returns an HTTP response with the error.
  - The client should receive the original Vault HTTP status code, including client-error statuses, instead of an Agent-generated 500.
  - The client should receive the original Vault response body and relevant response headers, rather than only the generic `failed to get the response:` wrapper.
- Responses that are not successful JSON Vault responses should pass through the caching listener without being treated as cacheable successes.
  - Unsuccessful upstream HTTP responses should be returned directly and should not become later cache hits.
  - Upstream responses that are not JSON responses should be returned directly and should not become later cache hits.
- Proxy failures that do not include a Vault HTTP response should continue to be reported as Agent-side failures.
  - In those cases, the listener should still return a 500 response using the existing `failed to get the response:` error context.

## Implementation notes

- Preserve the externally observable behavior of the caching listener: callers should be able to distinguish Vault-originated HTTP errors from Agent/proxy failures.
- The exact internal control flow, cache admission checks, and data structures are implementation details; choose whatever approach fits the existing codebase.
- Avoid changing unrelated request routing, authentication, or cache semantics beyond the rejection/pass-through behavior described above.
