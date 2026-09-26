The docs for `register_type_strategy` say that instead of registering `tuple[int]`, I can register `tuple` with a function that takes the type and return the strategy. I may be misunderstanding, but I take this to mean that I can register
`st.register_type_strategy(tuple, lambda typ: foo)`
and then `foo` should be the default strategy for _any_ param of type tuple, or `tuple[int]`, or `tuple[....]`, etc.

However, the code below results in a test failure, and from my investigation it is clear that the registration is not effective, and that `test` is getting any old `tuple[int]` rather than using the strategy that was registered.

```python
from hypothesis import given, strategies as st

# Note that I'm not actually using the typ param here, but I do use it in my actual code
st.register_type_strategy(tuple, lambda typ: st.tuples(st.integers(min_value=0)))

@given(x=...)
def test(x: tuple[int]):
    assert x[0] >= 0

test()
```

I'm not sure if I'm using this correctly or if I understand the correct behavior. Is it simply impossible to register a default strategy for tuples that will work on parameterized tuples? If so, the documentation seems to suggest otherwise to me. Also, this seems like a useful feature to have. Or, is it that I am doing something wrong?

Thanks!
