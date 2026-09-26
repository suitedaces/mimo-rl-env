## Create-user API rejects users that authenticate through a third-party identity provider

I'm integrating with the create-user API and trying to provision accounts for users who sign in via an external identity provider (SSO / OAuth). These users don't necessarily have an email address on file with us — the identity provider is their source of truth, and I pass that along in the `identities` array.

A request body like:

```json
{
  "authority": "example.com",
  "username": "jdoe",
  "identities": [
    {"provider": "acme-sso", "provider_unique_id": "user-12345"}
  ]
}
```

gets rejected by `CreateUserAPISchema` because `email` is listed as required. But for this class of user I genuinely don't have an email to supply — the whole point is that the third-party provider is handling identity for them.

I think `email` should only be required when the caller hasn't supplied an `identities` entry. If the request already pins the new account to one or more external identities, that should be a sufficient way to identify the user and `email` should be allowed to be omitted.

One related thing while looking at this: an empty `identities: []` shouldn't count as "the user has external identities" — if a caller goes the identities route, they should actually have to provide at least one. Otherwise you could omit `email` *and* pass an empty array and end up with a user that has neither, which doesn't make sense.

Could the schema be relaxed so that a request is accepted as long as it has `authority` + `username` and *either* an `email` *or* a non-empty `identities` array? Existing callers that pass `email` should keep working unchanged.

This affects both `h/schemas/api/user.py` (the runtime schema) and the published `new-user-schema.json` in the API reference docs.
