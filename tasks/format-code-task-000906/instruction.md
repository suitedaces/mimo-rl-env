[BUG] iter_to_str() misprint with two objects.
#### Describe the bug
<!--(Replace with a clear and concise description of what the bug is.)-->
`iter_to_str` inside `get_display_*`'s behaviour seems faulty.

With it's default separators (`sep","` , `endsep=", and"`), and 2 objects in the iterable, the in-game game return is `" and "` separating the names `(obj1 and obj2)`. While more than 2, returns `", and"`; `(obj1, obj2, and obj3)`.

Changing the default  `sep` to something like `sep="-"`, makes the return `X, and Y` as opposed to `X and Y` when there's 2 objects.

Apparenty, this happens whenever `sep` and `endsep` are the same (or `endsep` starts with the same character).
Got the same behavior with `[sep=',', endsep=',']`, `[sep='-', endsep='-']`, `[sep=';', endsep=';']`.
In these cases output with 2 objects is `X Y` as opposed to `X, Y`, for example.

#### To Reproduce
Steps to reproduce the behavior:
1. Overload any `get_display_*` function in an object.
2. Set it's `*_names` value's `iter_to_str` separator parameters as the same character. (e.g.: `sep","` , `endsep=","`)
3. Run the game and `look` in a place where there's two of anything (`Exits`, `Characters` or `Things`)
4. Check `look` output for misprint

#### Expected behavior
<!--(Replace with a clear and concise description of what you expected to happen.)-->
The presence of 2 objects in the iterable being used by `iter_to_str` should output the proper `endsep` string.
With the same separators parameters, output with 2 objects should be `X, Y`, not `X Y`.

#### Environment, Evennia version, OS etc
<!--(Replace with info. If unsure, run `evennia -v` or get the first few lines of the `about` command in-game.)-->
    Evennia 1.0.2
    OS: nt

#### Additional context
<!--(Replace with any other context about the problem, or ideas on how to solve.)-->
