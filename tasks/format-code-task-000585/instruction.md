## `rerun_filter` under pytest always receives `None` for err and name

I'm using flaky with pytest and trying to set up a `rerun_filter` so that only certain kinds of failures get retried (e.g. retry on a flaky network exception, but fail immediately on `AssertionError`).

Minimal repro:

```python
import pytest
from flaky import flaky

def my_filter(err, name, test, plugin):
    print("rerun_filter called with err=%r name=%r" % (err, name))
    # I want to inspect err[0] (the exception type) here to decide
    return True

@flaky(max_runs=3, rerun_filter=my_filter)
def test_something():
    assert False
```

When I run this under pytest, the filter does get invoked between reruns, but the output is always:

```
rerun_filter called with err=(None, None, None) name=None
```

No matter what the test actually raises, `err` is `(None, None, None)` and `name` is `None`. That makes it impossible to write a filter that branches on the exception type or on which test failed — the only signal the callback gets is "something failed, decide now", with no information about *what* failed.

I'd expect the same callback to receive the real exception info and test name (the way it does for the nose integration), so that filters like "retry only on `ConnectionError`" can actually be written.

flaky version: 3.0.1, pytest as test runner.
