## `set_to` context manager raises on exit for never-set parameters

I have a measurement script that uses `set_to` to temporarily change a parameter inside a `with` block. The parameter is created fresh at the start of the script — no `initial_value`, and I never call `.set()` on it before entering the block. Entering the block works fine, but the `with` statement blows up on exit.

Minimal repro:

```python
from qcodes.parameters import Parameter
from qcodes.validators import Numbers

p = Parameter("p", set_cmd=None, get_cmd=None, vals=Numbers(0, 10))

with p.set_to(3):
    # do measurement stuff at p=3
    pass
# <-- exception raised here when the context exits
```

If I `p.set(2)` (or set anything else) before the `with`, everything is fine and `p` is restored to `2` on exit as expected. The breakage is specifically when the parameter has never been assigned a value before entering the context.

This is annoying because in a lot of my scripts I bundle parameter creation and measurement together, and I'd like to be able to write `with some_param.set_to(x):` without having to remember to seed every parameter with a dummy value first. It's also a bit surprising — there's nothing in the user-visible contract of `set_to` that suggests the parameter needs to have been set previously for the context to work.

It would be nice if `set_to` could be used on an uninitialized parameter without erroring out at the end of the block.
