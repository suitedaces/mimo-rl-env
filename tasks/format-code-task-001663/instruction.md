# Problem Statement

When I deploy a CAAS charm onto certain series, the operator fails because it can't figure out the right charm-base OCI image to pull. I'd expect deploying on a valid series to consistently land on the correct `charm-base:<name>-<version>` image. Also, when I forget to set a base name somewhere, the validation error just says "base name not valid" which is pretty vague — it'd be nicer if it actually told me the name was empty.

# Expected outcomes

- CAAS charm deployment on a valid series should resolve a usable charm-base OCI image for that series, with the final image reference using the `charm-base:<name>-<version>` form.
- The exported `podcfg.ImageForBase` helper should build the correct charm-base OCI image path for a supplied charm base value.
- Stable charm base channels should produce image tags without an extra risk suffix; non-stable channels should include the risk suffix.
- If `podcfg.ImageForBase` is asked to build an image for a base with an empty name, the validation error should explicitly identify that the base name is empty.
- Existing validation for missing or invalid channel information should continue to reject invalid base channels.

# Implementation notes

The exact data flow, helper structure, and validation location are up to the implementer. Prefer consistent behavior for valid deployment series.

## Required public API surface (mechanical binding)

The following name and signature MUST be implemented exactly as listed; downstream Go tests mechanically bind this exported helper:

- `podcfg.ImageForBase` — `func ImageForBase(imageRepo string, base charm.Base) (string, error)` — the helper is compile-called with charm manifest base values.

## Required error handling contract

When the following error condition occurs, the implementation MUST behave as specified:

- **`podcfg.ImageForBase` receives a base whose `Name` is empty**: return a non-nil not-valid error whose rendered message is exactly `empty base name not valid` — this public validation message distinguishes the empty-name failure from the previous generic base-name failure.
