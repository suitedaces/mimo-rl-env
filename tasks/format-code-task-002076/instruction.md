### Regression: `np.set_printoptions` started returning a value

After upgrading numpy I noticed that `np.set_printoptions(...)` no longer returns `None` — it now returns some object back to the caller. As far as I know this function has always been a "side-effect only" call that returns nothing, and a lot of existing code (and doctests) rely on that.

Minimal repro in the REPL:

```python
>>> import numpy as np
>>> result = np.set_printoptions(precision=4)
>>> result
<Token var=<ContextVar name='format_options' ...> at 0x...>
>>> result is None
False
```

In the previous numpy version this same call returned `None`.

This is a problem for me because:

- I have doctests like `>>> np.set_printoptions(precision=4)` that previously produced no output, and now they fail because of the unexpected repr being printed.
- Code that does things like `assert np.set_printoptions(...) is None` or relies on chaining/ignoring the return value silently has its behaviour changed.

I don't think this return value was ever documented as part of the public API, so this looks like an unintended change. Could `np.set_printoptions(...)` go back to returning `None` like it always used to?
