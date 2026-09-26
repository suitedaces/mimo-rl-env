## Promote `gno lint` to a top-level subcommand

When I work on Gno realms I run the linter constantly — it's part of my normal write/test/lint loop, just like formatting and testing. But the linter currently lives under the `tool` subcommand group:

```
gno tool lint .
```

while the other commands I reach for the most are top-level:

```
gno fmt ...
gno test ...
gno run ...
```

This inconsistency shows up in a bunch of places once you start setting up an editor or a project Makefile. For example, my Emacs flycheck checker and my Vim `makeprg` both have to spell it out as `gno tool lint`, and our `examples/Makefile` does the same:

```make
lint:
	go run ../gnovm/cmd/gno tool lint -v .
```

It feels off that `lint` is treated as a secondary "tool" while `fmt` — which I use for the same kind of source-hygiene reasons — is right there at the top level. The `gno --help` output reinforces that distinction: `fmt`, `run`, `test` etc. are listed as primary subcommands, and `lint` is hidden one level deeper under `tool`.

I'd like `gno lint` to work as a top-level subcommand, on par with `gno fmt` / `gno test` / `gno run`, so that the linter is a first-class part of the CLI surface. The existing docs, examples, Makefile invocations, and editor integration snippets that currently say `gno tool lint` should be updated to match the new spelling.
