### Allow overriding the config directory, not just the config file

Right now the only way I can override where the CLI keeps its config is the `--configuration` flag, which expects the full path to the config file, e.g.

```
doppler --configuration=/some/path/.doppler.yaml me
```

This is awkward for a few reasons:

- I don't really care what the file is called — that's an internal detail of the CLI. The CLI already owns a *directory* (`~/.doppler/` by default), and the file inside it is something the CLI manages. Asking me to repeat the filename in every invocation feels backwards.
- It's easy to get the filename wrong (is it `.doppler.yaml`? `doppler.yaml`? something else?), and there's no real reason I should have to know.
- In setups where I want to point Doppler at a non-default location (custom mount, shared machine, container with a writable directory that isn't `$HOME`, etc.), I'd much rather say "use *this* directory" and let the CLI figure out the rest.

It would be nice to have a flag that just takes a directory, something I can use like:

```
doppler --<dir-flag>=/some/path me
```

…and have the CLI place its config file inside that directory like it normally does under `~/.doppler/`.

Existing behavior (default location of `~/.doppler/<file>`) should keep working unchanged when no override is passed.

I'd expect the new flag to be named something like `--config-dir`.
