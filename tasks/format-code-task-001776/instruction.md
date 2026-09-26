# Problem Statement

I'm using the ACME revoke-cert API with a reason in the request, and it feels weird that WFE can still be configured to just ignore it. Can we make valid revocation reasons get honored by default and drop the old `AcceptRevocationReason` switch so there's only one behavior?

# Expected outcomes

- Revocation requests submitted through the ACME revoke-cert API that include a valid, user-allowed reason code should have that reason honored without requiring any opt-in WFE configuration.
- Revocation requests that include a disallowed reason code should be rejected as malformed, with the public error message `unsupported revocation reason code provided`.
- WFE configuration should no longer expose or accept the `AcceptRevocationReason` switch; revocation reason handling should be fixed behavior rather than configurable behavior.
- The behavior should be consistent across the WFE variants that implement ACME certificate revocation.

# Implementation notes

- The exact internal location and structure of the validation and forwarding logic is up to the implementer.
- The change should preserve existing revoke-cert behavior for requests that omit a reason, while making supplied valid reasons effective by default.
- Avoid keeping a compatibility path that allows WFE configuration to disable valid revocation reasons.
