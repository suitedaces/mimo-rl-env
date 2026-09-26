## Feature request: a decorator that wraps a function in a Redlock

Right now if I want to make sure a function only runs one-at-a-time across
my workers, I have to wrap every call site (or the body of the function)
with the `Redlock` context manager:

```python
from pottery import Redlock

def refresh_cache():
    with Redlock(key='refresh-cache'):
        # ... actual work ...
        ...
```

This works, but it's boilerplate I end up repeating in a lot of places, and
indenting the whole function body just to hold a lock feels off — the lock
is really a property of the function itself, not of the body.

It would be nice if pottery shipped a decorator form so I could just write
something like:

```python
@some_decorator(key='refresh-cache')
def refresh_cache():
    # ... actual work ...
    ...
```

and have every call to `refresh_cache()` transparently acquire the Redlock
before running and release it after. The decorator should accept the same
knobs `Redlock` already accepts (the lock key, the redis masters to use,
the auto-release timeout) so I don't lose any of the existing flexibility.

I've been carrying a private version of this in my own app for a while and
it's been useful enough that I think it belongs in the library proper.

Naming-wise I'd expect the new helper to be importable from `pottery` as
something like `redlock` (the lowercase counterpart of the existing
`Redlock` class), so usage reads `from pottery import redlock`.
