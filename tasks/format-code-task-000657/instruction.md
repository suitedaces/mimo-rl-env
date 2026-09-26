Currently `opnieuw` will only raise the last caught exception. This creates two issues:
1. We lose any exceptions that were previously raised. This is especially problematic when the first caught exception is different from the second caught exception.
2. It is hard to tell whether `opnieuw` actually retried in a Sentry stack trace as the retrying isn't explicitly in the trace.

```python
from opnieuw import retry

counter = 0


@retry(
    retry_on_exceptions=(TypeError, ValueError),
    max_calls_total=3,
    retry_window_after_first_call_in_seconds=1,
)
def raise_depending_on_counter() -> None:
    global counter
    counter += 1
    if counter == 1:
        raise TypeError
    elif counter == 2:
        raise ValueError
    else:
        raise IndexError


raise_depending_on_counter()
```

This currently raises:
```console
❯ python test.py
Traceback (most recent call last):
  File "/home/daniel/channable/requestmachine/test.py", line 22, in <module>
    raise_depending_on_counter()
  File "/nix/store/mzflaklx9497sffvm5k28cf6m0zdi0yd-python3-3.11.4-env/lib/python3.11/site-packages/opnieuw/retries.py", line 240, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/home/daniel/channable/requestmachine/test.py", line 19, in raise_depending_on_counter
    raise IndexError
IndexError
```

Ideally it would be something like:
```console
❯ python test.py
Traceback (most recent call last):
  File "/nix/store/mzflaklx9497sffvm5k28cf6m0zdi0yd-python3-3.11.4-env/lib/python3.11/site-packages/opnieuw/retries.py", line 241, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/home/daniel/channable/requestmachine/test.py", line 15, in raise_depending_on_counter
    raise TypeError
TypeError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/nix/store/mzflaklx9497sffvm5k28cf6m0zdi0yd-python3-3.11.4-env/lib/python3.11/site-packages/opnieuw/retries.py", line 241, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/home/daniel/channable/requestmachine/test.py", line 17, in raise_depending_on_counter
    raise ValueError
ValueError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/daniel/channable/requestmachine/test.py", line 22, in <module>
    raise_depending_on_counter()
  File "/nix/store/mzflaklx9497sffvm5k28cf6m0zdi0yd-python3-3.11.4-env/lib/python3.11/site-packages/opnieuw/retries.py", line 265, in wrapper
    raise last_exception
  File "/nix/store/mzflaklx9497sffvm5k28cf6m0zdi0yd-python3-3.11.4-env/lib/python3.11/site-packages/opnieuw/retries.py", line 241, in wrapper
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "/home/daniel/channable/requestmachine/test.py", line 19, in raise_depending_on_counter
    raise IndexError
IndexError
```

A draft PR is here: https://github.com/channable/opnieuw/pull/21.
