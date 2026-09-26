# Problem Statement

I'm running Airbyte's HubSpot source on an account with a lot of custom contact/deal properties, and those streams keep failing with HubSpot HTTP 414 / `Request-URI Too Long`. Smaller HubSpot objects sync fine, so it looks like the connector is building a request URL that's too large when it includes all the properties.

# Expected outcomes

- HubSpot streams that need to request very large sets of object properties should split those properties across multiple requests conservatively enough to avoid a single request URL becoming too long.
- Property requests should remain safe for realistic HubSpot property names, including names that are not simple alphanumeric identifiers.
- Small property sets should continue to be requested normally without unnecessary behavior changes, and all requested properties should still be covered without dropping or duplicating them.
- Airbyte's HubSpot source definition/spec metadata should point at the fixed connector version: `dockerImageTag: 0.1.69`, `dockerImage: "airbyte/source-hubspot:0.1.69"`, and `LABEL io.airbyte.version=0.1.69`.

# Implementation notes

The exact internal structure, helper functions, and location of the URL-length checks are up to the implementer. The important behavior is that HubSpot property requests remain complete while avoiding overlong request URLs across both large and realistic property sets.
