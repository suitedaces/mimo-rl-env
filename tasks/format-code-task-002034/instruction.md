### Setup-key update API allows changing immutable fields and "un-revoking" a revoked key

Looking at the OpenAPI spec for `PUT /api/setup-keys/{keyId}` (the `SetupKeyRequest` schema), it advertises that you can update the key's `name`, `type`, `expires_in`, `usage_limit`, `ephemeral`, `revoked` and `auto_groups`. That doesn't match how setup keys actually work, and the current behavior creates two concrete problems for us:

**1. Fields that should be fixed at creation time appear mutable.**

A setup key is supposed to be defined at creation — its type (one-off vs reusable), its expiration window, its usage limit, whether enrolled peers are ephemeral, and its name are all properties of *that key*. Today I can `PUT` a new `name` to an existing key and the server happily accepts and persists it (I haven't checked the others carefully, but the spec implies they're all in play too). This is confusing for anyone integrating against the documented API: either these things are key properties that you commit to at creation, or they're mutable post-hoc — it can't be both. From the product standpoint they should be immutable; once a setup key is issued, the only things callers should be able to do are (a) put it in/out of groups and (b) revoke it.

**2. Revoked keys can be brought back to life via the same endpoint.**

`revoked` is currently just a boolean in the update payload, so if I send `{"revoked": false, ...}` against a key that was previously revoked, it un-revokes. Revocation is supposed to be a terminal state — once a key is revoked it should stay revoked. Otherwise "revoke" isn't really a security primitive. The endpoint should reject an attempt to flip `revoked` from true back to false.

**Ask**

Please bring the `PUT /api/setup-keys/{keyId}` endpoint (and its OpenAPI schema) in line with the actual lifecycle of a setup key: only the properties that genuinely make sense to mutate after creation should be exposed/accepted, and revocation should be one-way.

Repro for the un-revoke case:

```
# create a key, then:
curl -X PUT .../api/setup-keys/<id> -d '{"revoked": true,  "auto_groups": [...]}'   # ok, revoked
curl -X PUT .../api/setup-keys/<id> -d '{"revoked": false, "auto_groups": [...]}'   # currently succeeds — should not
```
