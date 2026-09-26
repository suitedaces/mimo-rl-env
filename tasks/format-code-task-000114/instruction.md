## Problem Statement

我这边用 `st.builds()` 生成一个 `typing.NamedTuple` 子类时，明明字段都写了类型注解，它还是没法自动推断构造参数，感觉像是把这个类的初始化签名看丢了。比如 `Point(NamedTuple)` 里有 `x: int`、`y: int`，我希望直接 `st.builds(Point)` 就能生成正常的 `Point` 实例，部分字段我手动传了的话也只补剩下的就好。

## Expected outcomes

- For a `typing.NamedTuple` subclass with annotated fields, `hypothesis.strategies.builds(target, *args, **kwargs)` should be able to infer strategies for missing constructor fields from those field annotations and generate valid instances of the NamedTuple subclass.
- When some NamedTuple constructor fields are supplied positionally or by keyword to `hypothesis.strategies.builds(target, *args, **kwargs)`, those supplied fields should be treated as already provided; inference should only be required for the remaining annotated fields.
- `hypothesis.strategies.from_type(thing)` should continue to resolve annotated `typing.NamedTuple` subclasses to strategies that generate valid instances of that subclass.

## Implementation notes

- The concrete detection mechanism, data structures, and validation location are left to the implementation, as long as the public strategy APIs above exhibit the expected behavior.
- Existing behavior for non-`typing.NamedTuple` targets should be preserved.
