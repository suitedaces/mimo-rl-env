我在用 `Annotated[MyModel, ...]` 这种写法，然后直接 `Annotated[MyModel, 'something']()` 去实例化，结果报了个 `ValueError: "MyModel" object has no field "__orig_class__"`。

奇怪的是单独 `MyModel()` 完全没问题，套上 `Annotated` 再调用就炸了。我啥也没改，就是想正常用 `Annotated` 包一下我的 model 而已。

Expected outcomes:
- `BaseModel` subclasses can be instantiated through `typing_extensions.Annotated[...]` aliases without raising an error related to typing metadata being attached to the created instance.
- Standard Python/typing metadata dunder attributes relevant to this kind of runtime metadata attachment should be assignable on a `BaseModel` instance and readable back from that instance, rather than being treated as ordinary unknown model fields.
- Such metadata attributes should not be exposed in the model’s user-facing representation, while normal model fields should continue to be represented as before.
- Existing validation and assignment behavior for ordinary field names and unrelated unknown attribute names should remain unchanged.

Implementation notes:
- Do not solve this by broadly allowing arbitrary unknown attributes on models.
- The internal location, data structure, or helper shape used to implement the behavior is up to the implementation, as long as the externally observable behavior above is satisfied.
