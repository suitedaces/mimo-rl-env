## Support JSON as a configuration file format

Right now Commitizen only reads its configuration from TOML files (`pyproject.toml` / `.cz.toml`). For Python projects that's fine, but I'm using Commitizen on a non-Python project (a JS codebase) where TOML is pretty foreign — none of our other tooling uses it, and contributors have to learn yet another format just to tweak commit rules.

JSON, on the other hand, is already everywhere in these ecosystems (`package.json`, tsconfig, eslint, prettier, …). It would be great if Commitizen could pick up a JSON config file the same way it picks up `.cz.toml` today, so I can drop something like `.cz.json` at the repo root and have it Just Work.

Concretely, I'd expect:

- All the same settings that work in `.cz.toml` (name, version, version_files, style, the whole `customize` block, …) to be expressible in JSON and behave identically.
- `cz init` to be a viable way to bootstrap a JSON config, not only a TOML one — i.e. if I'm in a JS project I shouldn't be forced to end up with a `.cz.toml`.
- `cz bump` and friends that write back to the config (e.g. updating the version) to keep working when the config happens to be JSON.

The docs currently say customization "is only supported when configuring through toml" — ideally that restriction would also go away once JSON is supported.

Related: #120
