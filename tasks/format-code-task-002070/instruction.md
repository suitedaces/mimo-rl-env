## Feature request: allow validating keys that aren't declared in `types`

I'm using `nopt` to parse arguments for a CLI tool. I declare the keys I expect via the `types` map and pass an `invalidHandler` to react to bad input. That works great for known keys.

The problem: if a user passes a flag that isn't listed in `types`, `clean` just keeps whatever string the user gave (after the basic null/true/false/number/date coercion) and lets it through. There's no way to apply any kind of validation to those unknown keys — `invalidHandler` never sees them.

In my CLI I'd like unknown flags to still be subject to a fallback type constraint (in my case I want to restrict them to a small set of allowed shapes, and reject anything else through my existing `invalidHandler`). Right now I have to post-process `data` myself after `nopt` returns, which is awkward because by that point I've lost the distinction between "user passed something weird" and "user passed something I never declared".

Could `nopt` (and `clean`) expose a way for the caller to supply a fallback type that gets applied to keys not present in `types`? When the caller doesn't supply one, behavior should stay exactly as it is today (unknown keys pass through untouched) so this is fully backward compatible.

Ideally `invalidHandler` would still fire for these unknown-but-now-validated keys when they fail, so a single handler can deal with both "declared key with bad value" and "undeclared key that doesn't fit the fallback".

The new option I'd expect would be something like `typeDefault`.
