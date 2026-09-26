# Problem Statement

I've got a bunch of Ignition configs floating around that still declare `"ignition": { "version": "2.0.0" }`, and when I feed them through `config.Parse` they blow up because it tries to read them as the latest schema. I don't really want to hand-rewrite them all to the newest version — can the parser just recognize 2.0.0 configs and handle them properly, ideally giving me back the same internal config type so the rest of my code doesn't care which version the input was?

# Expected outcomes

- `config.Parse` should accept valid Ignition configs that declare version `2.0.0`.
- Parsing a valid `2.0.0` config should return the repository’s current `types.Config` representation, so callers can consume it like configs parsed from newer supported versions.
- Supported user-visible configuration data from valid `2.0.0` configs should be preserved in the current config representation.
- Invalid `2.0.0` configs should still fail with an error and validation report rather than being silently accepted.
- Existing behavior for other supported versions should continue to work.

# Implementation notes

- Do not require callers of `config.Parse` to know whether the input was originally version `2.0.0` or a newer supported version.
- Prefer behavior-compatible integration with the existing config parsing and validation conventions.
- The exact parsing organization and compatibility implementation are up to the implementer.
