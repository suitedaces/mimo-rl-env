I’m using the Java SDK’s ManagementAPI and I need to trigger Auth0’s verification email job from there, but right now I don’t see any Jobs API support so I have to hand-roll the HTTP call. It would be great if the SDK let me send a verification email for a user and get back a typed job response I can inspect, like the job id/status/type and creation time.

Expected outcomes:
- Management API callers can access Jobs support through `ManagementAPI.jobs()`, receiving a `JobsEntity` that exposes Jobs-related operations.
- `JobsEntity.sendVerificationEmail(String userId, String clientId)` returns a `Request<Job>` for sending a verification email job for the given user.
- Executing the verification email request sends a POST request to Auth0’s verification email job endpoint, includes the required `user_id` in the JSON request body, and includes `client_id` only when a non-empty client id is provided.
- Calling the verification email operation without a user id is rejected by the SDK before sending a request.
- The SDK provides `com.auth0.json.mgmt.jobs.Job` for the Jobs API response, with readable `getId()`, `getStatus()`, `getType()`, and `getCreatedAt()` values from the response JSON.
- `Job` JSON handling ignores unknown response fields and does not serialize null fields.

Implementation notes:
- Follow the existing Management API entity and request patterns in the SDK.
- The internal data structures, validation location, and JSON binding details are up to the implementation as long as the public SDK behavior above is satisfied.

## Required output literals (exact-match contract)

When executing Jobs Management API requests, the implementation MUST authenticate the HTTP request using the configured API token:

- HTTP header name: `Authorization` - exact wire-level header required by the existing Management API request pattern.
- HTTP header value: `Bearer ` followed by the configured API token - exact bearer-token prefix required for Auth0 Management API authentication.
