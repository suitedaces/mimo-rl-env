mypy does not complain about async functions that do not return values
Found as part of https://github.com/python/mypy/pull/12834

In the following, you'd expect mypy to complain about assigning to `await async_nothing`, like it does with the synchronous case. Note that mypy does in fact complain about this using the old asyncio.coroutine yield from coroutines, see `testErrorAssigningCoroutineThatDontReturn` (prior to #12834).
```
def nothing() -> None:
    ...

def foo() -> None:
    x = nothing()  # E: "nothing" does not return a value

async def async_nothing() -> None:
    ...

async def async_foo() -> None:
    x = await async_nothing()
```
