### Wallet CLI commands print address values wrapped in a struct

I'm using `venus wallet ...` to manage keys on my node and the output of several commands is not really usable from the shell.

When I run

```
venus wallet new
```

I don't get a plain address back. The output comes out wrapped with a field name (looks like the command is dumping the underlying Go struct / its JSON form), so I can't just copy a clean `f1...` / `t1...` string and pipe it into the next command. Same thing happens with:

- `venus wallet default`
- `venus wallet set-default <addr>`
- `venus wallet import ...`

All of them should just print the address (or the exported key, for export) as a single line of text the way any other CLI does, so I can do things like

```
ADDR=$(venus wallet new)
venus wallet set-default $ADDR
```

without having to post-process the output.

### `wallet ls` output is too thin

Related: `venus wallet ls` currently just prints the list of addresses and nothing else. Compared to other Filecoin implementations this is pretty bare — when I have a handful of keys on a node I usually want to see, at a glance, which one is the default and roughly how much balance is on each, otherwise I have to follow up with a separate `wallet balance` call per address. Would be great if `wallet ls` showed that kind of summary by default, and still had a way to get just the plain addresses for scripting.

### Minor: typo in network params

While poking around the config I noticed `NetworkParamsConfig` has a field spelled `AdressNetwork` (missing a `d`). It's referenced from all the network presets under `fixtures/networks/*.go` as well. Looks like a straight typo and probably worth fixing while the wallet output is being cleaned up.
