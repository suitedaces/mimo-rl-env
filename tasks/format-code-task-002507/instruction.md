## `get_var_value` sometimes returns a `Var` instead of the actual value

I'm building a Reflex app and inside an event handler I call `await self.get_var_value(some_var)` to read the current value of a var so I can do plain Python work with it (compare it, pass it to a library, log it, etc.).

In most cases this works fine and I get back the expected Python value (a string, int, list, whatever the var holds). But for some vars I end up getting back a `Var` object instead of the underlying value, and the rest of my handler breaks because it's not a real Python value — I can't compare it, iterate it, or pass it anywhere that expects the resolved data.

Minimal shape of what I'm doing:

```python
class MyState(rx.State):
    async def do_something(self, target_var):
        value = await self.get_var_value(target_var)
        # expected: the actual Python value held by target_var
        # actual:   sometimes a Var object slips through here
        print(type(value), value)
        ...
```

I'd expect `get_var_value` to always give me the fully resolved Python value regardless of how the var was constructed — if it's a `Var` under the hood, it should be unwrapped before being returned to me, not handed back as-is.
