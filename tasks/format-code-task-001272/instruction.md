## Problem Statement

I’m creating/updating external team and user mappings through the API with an `external_id`, and the request succeeds, but when I fetch the mapping afterward the ID I sent isn’t there or hasn’t changed. Can you make `external_id` behave like a normal field on those requests, including rejecting obviously invalid values instead of silently losing them?

## Expected outcomes

- External team mappings: creating or updating a mapping with a valid `external_id` persists that provider-side ID and returns it on later reads.
- External user mappings: creating or updating a mapping with a valid `external_id` persists that provider-side ID and returns it on later reads.
- Optional field behavior: `external_id` may be omitted, or sent as `null`, on create and update requests; both are accepted and treated as no external ID.
- Validation behavior: invalid `external_id` values, including empty strings and values longer than 64 characters, are rejected with a validation error associated with `external_id`.

## Implementation notes

- The concrete serializer structure, helper functions, and validation location are up to the implementer.
- Keep the API behavior consistent across external team and external user create/update flows.
- Preserve existing public response shapes and validation semantics except where `external_id` handling needs to change.
