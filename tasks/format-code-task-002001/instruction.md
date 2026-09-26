## `unset` doesn't remove shell functions

I have a script that defines some helper functions and later calls `unset` to clean them up:

```sh
helper() { echo "doing helper stuff"; }
helper
unset helper
helper   # I want this to fail — function should be gone
```

Under bash, the final `helper` call fails (function no longer exists), but when I run the same script through mvdan/sh, the function is still defined and runs normally.

The same thing happens if I try `unset -f helper`, which is bash's explicit way of removing a function definition — it has no effect, and on top of that `-f` / `-v` don't seem to be recognized as flags at all (they get treated as names to unset).

Would be great if `unset` matched bash here so I can actually drop function definitions from a running script.
