## Problem Statement

I switch between a few different builders depending on the project I'm working on, and right now there's no easy way to manage my default builder from the `pack config` command. I'd love to be able to check what my current default builder is, set a new one, and clear it out when I don't want a default anymore — all through `pack config`. Ideally when I set one it'd make sure the builder actually exists first so I don't end up with a bogus default. Also, I keep typo-ing `pack config trusted-builders` as `trust-builder`, so it'd be nice if those just worked too.

## Expected Outcomes

- `pack config default-builder` reports the saved default builder when one exists, and reports that none is set with guidance toward suggested builders when it does not.
- `pack config default-builder <builder-name>` only saves a builder after confirming it can be found; if it cannot be found, the command fails clearly and leaves the previous default unchanged.
- `pack config default-builder --unset` and `pack config default-builder -u` clear a saved default builder, or report that there was nothing to clear.
- `pack config trust-builder` and `pack config trust-builders` behave as aliases for the existing `pack config trusted-builders` command, including its subcommands.

## Implementation Notes

Keep the behavior observable through the CLI and persisted pack configuration. Preserve existing `pack config` behavior while adding the new default-builder management flow and trusted-builder aliases; command wiring, validation placement, helper names, and internal data organization are up to the implementation.
