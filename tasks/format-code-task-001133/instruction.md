## Stable Web App Manifest identities

Lighthouse's manifest parser normalizes fields such as `start_url`, but it does not expose the Web App Manifest `id` member. That leaves audits and report consumers unable to tell whether an app declares a stable identity instead of implicitly tying identity to a launch URL that may change. Add normalized manifest identity support and surface it as a non-scoring PWA best-practice audit.

The parsed manifest artifact must include an `id` node with the same observable `raw`, `value`, and optional `warning` shape used by other parsed members. Treat the already-normalized effective `start_url` as the base and fallback identity. A string `id` is a URL reference resolved against that start URL, not against the manifest URL. Remove its fragment from the normalized identity while preserving the rest of the URL, including its query. An explicitly empty string is valid and resolves to the fragment-free start URL.

When `id` is omitted, use the fragment-free effective start URL without a warning and preserve `raw` as `undefined`; this also applies when `start_url` itself defaults to the document URL. A non-string, an unparseable URL reference, or a resolved URL that is not same-origin with the start URL must fall back to that same fragment-free identity while preserving the original raw input. These invalid explicit values must carry a useful warning: respectively mention that a string was expected, identify an invalid `id`, or mention the same-origin requirement. Same-origin comparison includes scheme, hostname, and port.

Expose a `hasId` entry through the existing ManifestValues computed result. Its failure text must mention `id`. It passes only when an explicit `id` was supplied and parsed without an identity warning; in particular, an explicit empty string passes, while an omitted or invalid value fails.

Add a binary navigation audit whose public ID is `manifest-id`. It scores 1 exactly when the `hasId` condition passes and 0 for omitted or invalid IDs. A missing or unparseable manifest also scores 0 and includes a non-empty explanation of the manifest failure. Make the audit available in the default audit set and add it to the PWA category's `pwa-optimized` group with weight 0, so it is visible without changing the PWA score.

Keep all existing parsing, ManifestValues checks, and default-config behavior unchanged for manifests and audits unrelated to identity.
