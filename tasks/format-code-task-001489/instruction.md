# Problem Statement

I'm working on the deCONZ integration and trying to move it over to the config entries flow instead of the old discovery-based platform loading. The problem is when I call `hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")` (and same for `sensor` and `scene`), it doesn't work — those base components don't seem to support being set up from a config entry the way `light` does. Could we get these entity platforms to participate correctly in the config-entry setup flow, so integrations like deCONZ can register their entities through the config-entry platform setup path instead of relying on legacy discovery loading?

# Expected outcomes

- Config-entry forwarding support:
  - Forwarding a config entry to `binary_sensor`, `sensor`, or `scene` through `hass.config_entries.async_forward_entry_setup(...)` should succeed when the target integration exposes platform setup for config entries.
  - The `binary_sensor`, `sensor`, and `scene` base components should support Home Assistant’s existing config-entry forwarding flow for entity platforms.

- deCONZ config-entry setup:
  - Setting up deCONZ from a config entry should initialize the bridge from the config entry data.
  - deCONZ’s config-entry setup should reach its supported entity platforms through the config-entry platform setup flow.
  - During config-entry setup, deCONZ should not also load those entity platforms through the legacy discovery path.

- deCONZ platform behavior:
  - deCONZ entity platforms should add the same entities from bridge data when invoked through the config-entry platform setup path as they previously did through the discovery-based path.
  - The legacy discovery-based platform setup path should not create duplicate entities for deCONZ after this migration.

- Existing deCONZ guard behavior:
  - Attempting to set up a second deCONZ config entry while one is already registered should still fail and report that a deCONZ instance already exists.

# Implementation notes

- Match the existing Home Assistant config-entry forwarding conventions for entity platforms.
- The exact organization of helper functions, intermediate data structures, and setup code is up to the implementer as long as the externally observable setup behavior above is satisfied.
- Preserve existing entity creation semantics for deCONZ platforms; this task is about how those platforms are reached and invoked, not changing which deCONZ entities are created from bridge data.
