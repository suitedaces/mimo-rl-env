# Problem Statement

I'm hitting some weird inconsistencies with error handling across the different framework integrations. When I send a GET request with malformed JSON in the query params to my aiohttp, asgi, and fastapi GraphQL views, I get a 500 / unhandled crash instead of any kind of clean error. Same thing with multipart uploads — if the JSON in operations/map is broken, or if my file map references a file that isn't actually in the form data, the asgi/django/fastapi views just blow up with an unhandled exception. Also on fastapi, when I hit the GraphQL endpoint with no query at all and GraphiQL turned off, I'm getting a 400 back which feels off. I'd like the error behavior to be consistent across all these integrations.

# Expected outcomes

- Malformed JSON supplied as request data, including through GET query parameters and multipart upload metadata, should be converted into a clean client-error HTTP response instead of escaping as an unhandled server error.
- Multipart upload requests that reference files missing from the submitted form data should also produce a clean client-error HTTP response instead of crashing.
- The affected integrations described above should expose consistent HTTP-level behavior for these malformed request cases:
  - malformed JSON request data returns HTTP 400 with the visible text `Unable to parse request body as JSON`;
  - missing multipart files return HTTP 400 with the visible text `File(s) missing in form data`.
- For the FastAPI GraphQL endpoint, a GET request with no GraphQL query when GraphiQL is disabled should no longer be treated as a bad GraphQL request; it should return HTTP 404.

# Implementation notes

- Preserve existing successful GraphQL request behavior while changing only the externally visible error behavior described above.
- Use each framework’s normal response/error mechanisms as appropriate.
- The exact internal control flow, helper placement, exception handling structure, and shared-vs-integration-specific implementation choices are up to the implementation; tests should observe HTTP-level behavior rather than a particular internal implementation path.
