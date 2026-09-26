## `secrets-config` CLI rough edges in EdgeX 3.0

I'm bringing up EdgeX 3.0 and using `secrets-config proxy` to add an API gateway user and install a TLS certificate. A few things made this harder than it should be.

### 1. `--help` looks like it errored out

For any of the proxy subcommands, e.g.

```
secrets-config proxy adduser --help
secrets-config proxy tls --help
secrets-config proxy deluser --help
```

I get the usage text I expected, but right after it there's a logged error line that makes it look like the command actually failed. As a user just trying to discover what flags exist, this is really confusing — asking for help shouldn't be reported as a failure. I'd expect `--help` to print usage and exit cleanly with no error output.

### 2. `cmd/secrets-config/README.md` doesn't match what the EdgeX 3.0 binary actually accepts

I tried following the README to figure out the right invocation. Several things documented there are rejected by the binary — subcommands and flags listed in the docs simply aren't there anymore, and some real flags on the supported subcommands aren't documented. The README also still says "Last change: 2020", so it looks like it just hasn't been brought forward for the 3.0 release.

Could the README be refreshed so it reflects what the binary supports today (and notes anything that was intentionally removed/renamed going into 3.0)?

### 3. `proxy tls` flag names are stylistically inconsistent with sibling subcommands

`proxy adduser` and `proxy deluser` use camelCase flags (`--useRootToken`, `--tokenTTL`, `--jwtTTL`, etc.), but `proxy tls` is all lowercase (`--incert`, `--inkey`, `--targetfolder`, `--certfilename`, `--keyfilename`). It's jarring when scripting both commands side by side. It'd be nice if the `tls` flags followed the same convention as the others.
