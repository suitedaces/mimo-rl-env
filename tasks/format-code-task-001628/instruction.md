## Typos / invalid values in keybinding config crash lazygit mid-session instead of failing at startup

I was customizing my keybindings in `~/.config/lazygit/config.yml` and made a typo on one of them — I tried to bind something to a key name lazygit doesn't recognize (I was guessing at the syntax for shift+arrow, but the same thing happens with any typo, e.g. `<ctrl-x>` instead of `<c-x>`).

lazygit launches fine. The trouble is that nothing tells me the config is broken until I actually trigger the affected keybinding during a session — at which point the whole TUI just exits with a one-line error about an unrecognized key. I lose whatever I was in the middle of (e.g. a half-staged commit), and from a user's perspective it looks like lazygit randomly crashed.

It would be much better if invalid keybinding values were caught when the config is loaded at startup, so I get a clear error up front pointing at which keybinding has the bad value and where to look up the valid key names. That way I can fix the typo before launching into a session.

A few related things I noticed while digging into this:

- The same lack of validation applies to keys configured under `customCommands` — if the `key:` there is misspelled, you only find out when you try to invoke it.
- Some entries under `keybinding.universal` are expected to be lists of a specific size (e.g. `jumpToBlock`). If you accidentally give it the wrong number of entries, you again don't find out until much later, in a more confusing way. These should also be sanity-checked at startup.
- The "Possible keybindings" table in `docs/keybindings/Custom_Keybindings.md` seems to be missing some keys that are actually accepted by the code (shift+arrow keys, backtab, alt+enter). Since the docs are how users figure out what to write in the config, it'd be good to have these listed so people don't have to guess.

In short: please validate keybinding-related config values at load time with a useful error message, and make sure the docs cover everything that's actually supported.
