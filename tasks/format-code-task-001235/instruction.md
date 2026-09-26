# Problem Statement

Right now when a Shoot fails to reconcile because of bad cloud credentials, everything seems to get bucketed into `ERR_INFRA_UNAUTHORIZED` — so I can't tell from the status whether the credentials were straight-up rejected (wrong access key, auth failed) versus the credentials being valid but lacking the right permissions on the provider side. Those are two totally different things I'd handle differently (rotate the key vs. fix the IAM policy), but the error code doesn't distinguish them. Could there be a separate code specifically for the "credentials didn't authenticate" case so I can route alerting on it? Also `ERR_INFRA_INSUFFICIENT_PRIVILEGES` shows up too and it's never been clear how it relates to the unauthorized one — would be nice if the docs made the relationship and meaning clearer.

# Expected outcomes

- Authentication vs. authorization:
  - Infrastructure errors caused by credentials that fail authentication, such as invalid access keys or authentication failures, should be classified with a distinct exported error code, `ERR_INFRA_UNAUTHENTICATED`.
  - Infrastructure errors caused by authenticated requests that are not authorized, such as access-denied or forbidden-style provider responses, should continue to be classified as `ERR_INFRA_UNAUTHORIZED`.
  - `DetermineErrorCodes` should distinguish these two categories so callers can route alerts differently for authentication failures versus authorization failures.

- Public error-code surface:
  - The public API should expose an `ErrorInfraUnauthenticated` error code whose string value is `ERR_INFRA_UNAUTHENTICATED`.
  - The new unauthenticated infrastructure code should be treated consistently with the existing non-retryable infrastructure credential/permission error codes.
  - `ERR_INFRA_INSUFFICIENT_PRIVILEGES` should remain understandable as a legacy/deprecated code whose meaning is covered by `ERR_INFRA_UNAUTHORIZED`.

- Documentation:
  - The Shoot status documentation should list `ERR_INFRA_UNAUTHENTICATED` and describe it as the code for missing or invalid authentication credentials.
  - The documentation for `ERR_INFRA_UNAUTHORIZED` should describe authorization refusal rather than invalid credentials.
  - The documentation for `ERR_INFRA_INSUFFICIENT_PRIVILEGES` should make clear that it is deprecated in favor of `ERR_INFRA_UNAUTHORIZED`.

# Implementation notes

The concrete implementation approach is up to the implementer. Choose whatever data structures, matching rules, and integration points fit the existing codebase, as long as the externally visible error-code classification, public constants, non-retryable handling, and documentation behavior match the outcomes above.
