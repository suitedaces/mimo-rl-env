Ignore excluded signatures when scanning
## Feature Request

## Is your feature request related to a problem? Please describe.

Right now, when a scan is performed, if you have `exclude-signatures` in your config, they will show up (rightly so) as entropy matches. While this is just a side effect of tartufo doing its job very well, it doesn't make for a great user experience, and it means that every user needs to explicitly exclude their config file from scans.

While excluding config files does work, it can be potentially problematic. Take Python projects, for example, where you can configure tartufo via the `pyproject.toml` file. Do we really want users to have to exclude that file, and simply assume that no other config in there could possibly contain secrets? What if we eventually support other config files, like `Cargo.toml` for example? Overall the current solution is not so great.

## Describe the solution you'd like

Since tartufo itself has a definitive list of all signatures to be excluded, it should be easy enough to look for any entropy matches in that list, and not report on them.

## Describe alternatives you've considered

The other solutions I considered were:

* Auto-ignore the config file, which is bad for the reasons covered above
* Use the new `--exclude-entropy-patterns` feature to ignore BLAKE2 hashes. But this could very easily be far too wide of a net.

## Teachability, Documentation, Adoption, Migration Strategy

Adoption for this should be automatic. Since this is really a feature to fix a bug, there shouldn't be too much necessary aside from the changelog entry.
