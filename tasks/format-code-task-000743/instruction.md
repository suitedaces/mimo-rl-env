## Dagger fails to load git config when `~/.gitconfig` contains a multi-line value

I have a few entries in my `~/.gitconfig` whose values span multiple lines (e.g. an `insteadOf` rewrite with an embedded newline, plus a signing key block). Standard `git` tooling handles these fine, but as soon as Dagger needs to read the git config (for example when resolving a private repo via an `insteadOf` rule), the operation fails.

The error surfaces as something like:

```
Failed to parse git config invalid format: line "..." doesn't match key=value pattern
```

…where the quoted line is the *second* line of one of my multi-line values — so it has no `=` in it, and the parser bails out on the whole config.

Running `git config -l` directly in the same shell prints the config without complaint, so the values themselves are valid; it just looks like Dagger's parsing of the output doesn't handle entries whose value contains a newline. The end effect is that any feature relying on `GetConfig` (insteadOf URL rewriting, etc.) is unusable for users with this kind of `.gitconfig`.

Could Dagger be made to read git config in a way that tolerates multi-line values? Stripping or rejecting those entries isn't really an option on my side — they're legitimate git configuration.
