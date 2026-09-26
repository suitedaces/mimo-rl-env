Provide a way to chain Err to Exception
Hi,

Thanks for a cool library. I've tried to find a solid way to manage error cases in Python like Rust and found this elegant library.

We're migrating some of our APIs using result and miss a feature to cover some common patterns we've found. As our library clients may not want to change their code base to be aware of `result.Ok` or `result.Err` (I hope so in the future though), we've decided to change our internal APIs only as a initial step.

So basically we have some of similar codes like

```python
# Internal API
def _get_user() -> Result[User, str]:
    ...

def _raise(e):
    raise e

# Public API
def get_user():
    return _get_user().map_err(lambda e: _raise(UserNotFoundException)).unwrap()   
```

This code works but have several ugliness including
- As lambda could not accept `raise`, we could not help to have a weird wrapper function like `_raise`
- We broke `map_err()` signature as the function accept a callable to return Err value

So basically, I'd like to ask having such API like below

```python
def get_user():
    # Return user when Ok otherwise raise UserNotFoundException which accepting error
    return _get_user().ok_or(UserNotFoundException)
```

I don't think `ok_or()` is a right API name to reflect the feature (and is different from `ok_or()` in Rust), so please understand the intention only. It seems opposite API of `as_result()` as it translates `Exception` to `Result` and now I'm asking a API for `Result.err` to `Exception`.

I think introducing `Try` API may be the right one to implement such feature but do not aware of the project's road map, so any viable solution would be appreciated.

Thanks!
