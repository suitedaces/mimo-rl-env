I'm running a Starlette app under `/api`, and inside a handler `request.url_for("user", id=123)` is giving me an absolute URL without that prefix, so the link points to a route that doesn't exist from the outside. I also hit this when trying to write a `TestClient` test for the same setup, because the app always sees an empty `root_path`.

Expected outcomes:
- URL generation with deployment prefixes:
  - When a request is handled under an externally visible root or mount prefix, `request.url_for(name, **path_params)` should return an absolute URL that includes that prefix.
  - Reverse URL generation should continue to work for routes both at the application root and inside mounted sub-applications.
- Request base URL:
  - `Request.base_url` should expose the current request’s scheme, host, and application root as a base URL, without including the current request path or query string.
  - The base URL should preserve the root path that external clients use to reach the application.
- TestClient root path simulation:
  - `TestClient(app, root_path="...")` should allow tests to simulate an ASGI `root_path`.
  - The configured root path should be visible to the application for HTTP requests and WebSocket connections.
- URL construction from ASGI scopes:
  - Constructing a `URL` from an ASGI scope that does not include `query_string` should treat the query string as empty instead of failing.

Implementation notes:
- The specific internal data flow, caching strategy, and validation locations are up to the implementation.
- Preserve existing public behavior outside the root-path and URL-construction cases described above.
- Avoid making tests depend on private helpers or internal adapter details; the intended behavior should be observable through Starlette’s public request, URL, routing, and test-client APIs.
