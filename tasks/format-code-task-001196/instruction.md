## Strict isinstance check rejects values that the transformer could actually convert

I have a task that takes a `FlyteFile` input:

```python
from flytekit import task, workflow
from flytekit.types.file import FlyteFile

@task
def process(f: FlyteFile) -> int:
    with open(f, "r") as fp:
        return len(fp.read())

@workflow
def wf(path: str) -> int:
    # I'd also like to be able to just hand a path string in directly
    # when driving things programmatically / locally
    return process(f=path)
```

When I try to drive this with a plain string path as the value for the `FlyteFile` input, flytekit blows up with a `FlyteTypeException` complaining that `str` is not an instance of `FlyteFile`. The conversion never gets a chance to run, even though the registered transformer for `FlyteFile` is perfectly capable of turning a path string into the right literal.

I'd expect the type engine to attempt the conversion through the registered transformer and only raise `FlyteTypeException` if the transformer itself can't handle the value. Right now anything that isn't already an `isinstance` of the declared type is rejected up front, which makes it impossible to leverage transformers that do legitimate type coercion (path-like → file, etc.).

Could the type engine be a bit less eager about the up-front isinstance check, and let the transformer have a say in whether the value is acceptable?
