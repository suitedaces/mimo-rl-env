`kompose -f <file> convert` doesn't pick up the compose file

I was trying out kompose for the first time and followed the examples in the user guide. The docs show the `-f` / `--file` flag used like this:

```console
$ kompose -f docker-gitlab.yml convert -y
```

and

```console
$ kompose --file ./examples/docker-guestbook.yml up
```

So I tried the same pattern with my own file:

```console
$ kompose -f my-compose.yml convert
```

This doesn't behave the way the docs suggest. kompose acts as if `-f` wasn't passed at all — it falls back to looking for the default `docker-compose.yml` in the current directory instead of reading `my-compose.yml`. Same thing with `kompose --file foo.yml up` and `kompose -f foo.yml down`.

If I instead put the flag *after* the subcommand:

```console
$ kompose convert -f my-compose.yml
```

then it works fine and my file gets picked up.

This is a bit confusing because every example in `docs/user-guide.md` puts `-f` / `--file` before the subcommand (`kompose -f ... convert`, `kompose --file ... up`, `kompose --file ... down`), so I assumed that was the intended invocation style. Either the docs are wrong, or the flag placement shown in the docs should actually work — I'd expect the latter since it reads more naturally (`-f` selects the input, the subcommand chooses what to do with it).

Could `-f` / `--file` be made to work when placed before the subcommand, like the documentation shows?
