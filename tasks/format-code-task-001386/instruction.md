## `--strict` ignores my lint configuration

I'm running `dashboard-linter lint` in CI with `--strict` and a configuration file (next to the dashboard) that excludes a few rule violations we can't address right now.

When I run the linter locally without `--strict`, the report correctly shows those violations with the excluded marker (➖), exactly as I'd expect from my config.

But the same command with `--strict` still exits non-zero, so my CI build fails — as if the exclusions in the config weren't applied at all.

I'd expect `--strict` to honor the configuration the same way the printed report does. If a violation has been excluded (or otherwise downgraded below the strict threshold) per the config, it shouldn't cause strict mode to fail.

(For what it's worth, on the API side I'd expect something like a `Configure` entry point on the result set so the configuration is applied consistently regardless of whether results are added before or after it.)
