## Problem Statement

Right now when something goes wrong inside my agent func — like I throw a ValueError, or someone hits a func name I haven't registered — Fixie just sees a generic 500 (or a plain 404 for the unknown func case) and there's no way for me to surface a real error message back to the user. I'd really like to be able to raise some kind of structured agent error from inside my func and have it come back as a proper AgentResponse with an error code and a message I control, instead of getting swallowed into an HTTP 500. The unknown-func case should probably do the same thing by default so the caller actually gets a useful payload back.

## Expected Outcomes

- Expose a public structured agent exception type, `AgentException`, that user code can raise with a user-facing response message, an error code, an error message, an intended HTTP status, and optional diagnostic details.
- Structured agent errors raised while handling an agent request are returned to the caller as an `AgentResponse` payload containing the user-facing message plus structured error code/message data, while preserving the intended HTTP status.
- Calling an unregistered func returns a structured `AgentResponse` error payload rather than a plain missing-route response; the payload identifies the requested missing func and gives the caller useful default unknown-func error information.
- Ordinary unhandled exceptions from agent func execution are converted into a valid `AgentResponse` error instead of escaping as an unstructured server failure.
- `UserStorage` cannot be used for anonymous end-user requests; attempts to do so fail with a structured agent error rather than succeeding or surfacing as an unstructured failure.
- Public argument-mapper integrations receive verified request claims through `VerifiedTokenClaims`, including enough verified context for custom argument mappers and built-in injected arguments to distinguish the agent identity, bearer token, and whether the request is anonymous.

## Implementation Notes

- Keep the external contract centered on request/response behavior and public SDK types; the concrete exception plumbing, validation location, and data structures are implementation choices.
- Do not regress existing successful agent responses, token validation behavior, func registration behavior, or streaming response behavior while adding structured error reporting.
- The structured error payload should be usable by callers without relying on private SDK internals.
