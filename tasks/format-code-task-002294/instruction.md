# Support yearly subscription tiers

Right now every subscription tier is implicitly billed monthly. We want to let
maintainers offer tiers that are billed **yearly** as well.

Introduce a `recurring_interval` on subscription tiers. The interval is one of
two values, `"month"` or `"year"`.

Expected behavior:

- When creating a tier, the caller may pass `recurring_interval` in the create
  payload. It is optional and defaults to `"month"` when omitted. Only `"month"`
  and `"year"` are accepted — any other value is a validation error (HTTP `422`).
- The interval a tier was created with is stored and returned as
  `recurring_interval` everywhere a subscription tier is serialized by the API
  (e.g. when creating, looking up, or listing tiers).
- The automatically-managed **Free** tier is always billed monthly.
- The tier listing/search accepts a `recurring_interval` filter: when a caller
  asks for a given interval, only tiers with that interval are returned; when no
  interval is given, tiers of every interval are returned.

Existing tiers and existing API callers that don't mention an interval must keep
working exactly as before (i.e. they behave as monthly tiers).
