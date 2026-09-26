I'm using Litestar's session middleware with a server-side backend (Redis) and I noticed that when a user "logs out" and I try to wipe their session, the data is still sitting in Redis afterwards — I can fetch it back by the same session id. The response does send a cookie that looks like it's clearing things on the browser side, but server-side nothing seems to actually get deleted. I've been trying to clear it by assigning an empty dict to the session, and I also tried setting it to `Empty` but the type checker complains that `set_session` doesn't accept that. Separately, while writing tests for this with `create_test_client`, passing my server-side `BaseBackendConfig` into `session_config=` also gets flagged because it only wants `SessionCookieConfig`.

Expected outcomes:
- Session clearing through the public connection API supports `ASGIConnection.set_session(Empty)` as a valid way to mark the session empty.
- Clearing a session, including by setting it to an empty value, removes the corresponding server-side session data so the same session id cannot retrieve the old contents later.
- Clearing a session still sends the browser-side clearing cookie, but does not also send a cookie carrying serialized session payload for the cleared session.
- `create_test_client(..., session_config=...)` accepts server-side session backend configuration types derived from `BaseBackendConfig`, not only cookie-session configuration.
- Test-client session inspection for a missing or already-cleared server-side session returns an empty dictionary instead of raising while trying to read absent data.

Implementation notes:
- Preserve the existing public session semantics for non-empty sessions.
- The exact validation location, storage operation flow, and internal data structures are up to the implementation.
- Keep the fix backend-agnostic: cookie-backed and server-side-backed sessions should each expose the expected external behavior without relying on a particular storage provider.
