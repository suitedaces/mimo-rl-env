## False positive "undefined variable" inside `elseif` branch when the condition uses `isset`

I'm running noverify on a fairly small PHP file and it's flagging variables as undefined in an `elseif` branch even though I clearly guard them with `isset` in that same `elseif`'s condition.

Roughly what my code looks like:

```php
<?php
function lookup($key) {
    if (isset($_GET['name'])) {
        return $_GET['name'];
    } elseif (isset($_GET['fallback'])) {
        return $_GET['fallback'];   // <-- noverify complains about $_GET['fallback'] / the guarded var here
    }
    return null;
}
```

When I run noverify on this, the `elseif` branch produces an "undefined variable" style warning for the variable that I just guarded in the `elseif (isset(...))` condition. The same pattern written as a plain `if (isset(...)) { ... }` does **not** get flagged, so the linter clearly understands `isset` as a presence guard in the `if` head — it just doesn't seem to apply that understanding to `elseif` heads.

Practically this is a problem because the `if / elseif / elseif / else` chain with one `isset` per branch is an extremely common PHP idiom (config lookups, request param fallbacks, polymorphic dispatch on which key is present, etc.), and right now any project using that pattern gets a wall of false positives that drown out real issues. Wrapping each branch with an extra outer `if (isset(...))` just to silence the linter defeats the point of using `elseif`.

I'd expect noverify to treat a guard in the `elseif` condition the same way it already treats a guard in the leading `if` condition: inside that branch's body, the guarded variable should be considered defined and shouldn't trigger the warning.
