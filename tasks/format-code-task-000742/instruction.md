# Support PEP 484 type hints in generated docstrings

Pyment builds docstrings from a function/method definition, but it currently
ignores the type annotations written in the signature. If a function is defined
with type hints, those types should be carried into the docstring it produces.

Please make the docstring generation read PEP 484 annotations from the
signature and reflect them in the output.

Concretely, for a function such as:

```python
def func(param1, param2: str = 'default val') -> int:
```

generating a reStructuredText docstring should produce, in addition to the
usual `:param ...:` fields:

- a `:type param2: str` field for the annotated parameter, and
- an `:rtype: int` field for the return annotation.

Requirements:

- A parameter that carries an annotation gets a corresponding type field; a
  parameter with no annotation gets no type field (the existing type-stub
  behaviour is unchanged).
- A return annotation (`-> ...`) becomes the return type of the docstring.
- An annotated parameter that also has a default value keeps its
  `(Default value = ...)` note; its type comes from the annotation.
- Annotations whose text contains commas inside brackets — e.g.
  `Dict[str, int]`, `Tuple[int, ...]`, `Optional[List[str]]` — must be treated
  as a single type and not split apart on the inner commas.
- A type that is already written in the source docstring wins: when the input
  docstring already specifies a parameter's type (or the return type), the
  signature annotation must not overwrite it.
- Methods still skip `self`/`cls`, and `async def` is handled like `def`.

This should work the same way for the styles Pyment already supports (reST,
javadoc, numpydoc, google): whenever a style renders parameter types and a
return type, the values inferred from the signature are used.
