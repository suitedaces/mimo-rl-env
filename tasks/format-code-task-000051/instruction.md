## Problem Statement

When I write a `file_owner` rule, I'm stuck specifying the expected owner as a literal numeric UID via `fileuid`. That's brittle for accounts whose UID isn't guaranteed to be the same everywhere — I really just want to say the owner should be `root` (or some other username) and have the check figure out the actual UID at scan time. Could the template accept a username there too, not just a hard-coded number?

## Expected outcomes

- The `file_owner` template supports a `uid_or_name` variable for the expected owner.
- A `uid_or_name` value that is a numeric UID continues to generate owner checks equivalent to the previous numeric-UID behavior.
- A `uid_or_name` value that is a username generates a check that compares against that account’s UID as resolved on the scanned system, so the same rule can work across systems where the account has different numeric UIDs.
- Bundled OpenShift rules that use the `file_owner` template express their expected owner through `uid_or_name` instead of the old numeric-only `fileuid` variable, without changing which owner they require.

## Implementation notes

The exact implementation strategy, data flow, and validation location are up to the implementer. Preserve the existing `file_owner` template behavior for path matching, recursive checks, and regular-expression-based file selection while extending only how the expected owner can be specified.
