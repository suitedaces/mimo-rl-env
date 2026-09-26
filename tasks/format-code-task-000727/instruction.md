## Feature request: drop-in configuration files

I'm packaging CRI-O for our distribution and want to ship sensible defaults in `/etc/crio/crio.conf` while letting users (and our config management) layer in machine-specific tweaks — custom registries, an extra runtime entry, a different cgroup manager — without ever touching that base file.

Today the only knob we have is `--config, -c` pointing at one TOML file, which forces us into two awkward options:

- Have users edit `/etc/crio/crio.conf` directly: conflicts on every package update, painful for config management to template.
- Have users replace it with their own copy: they lose any new defaults we ship in future releases.

Most other system daemons (systemd, networkd, sshd, …) solve this with a "drop-in" directory pattern: a directory of partial config files that are merged on top of the base config in a predictable order. I'd like CRI-O to support the same idea — a directory of partial TOML configs that get layered on top of the main `crio.conf` at startup, with ordering determined by filename so admins can pick priority via prefixes like `00-…`, `10-…`, `99-…`.

What matters for this to be useful:

- The base config file is applied first, then each fragment is layered on top in deterministic name order. Each fragment is just a partial TOML — only the keys it sets should take effect, the rest fall through to the lower-priority layers.
- Command-line flags passed to `crio` continue to have the highest priority, same as today, so a CLI override always beats both the base config and any fragments.
- If the drop-in directory doesn't exist, startup should not fail — that's the expected state for users who don't use drop-ins at all.

This would let distros and config-management tools layer overrides cleanly without ever rewriting `crio.conf`.

A natural shape would be a new CLI flag like `--config-dir` (short `-d`) on `crio` to point at the directory, plus a corresponding method on the `Config` type (something like `UpdateFromPath`) that walks the directory and layers each file on top via the existing per-file update path.
