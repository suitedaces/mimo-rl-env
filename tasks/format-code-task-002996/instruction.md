## WPS221 fires on PEP695 `type` aliases

I'm on Python 3.12 and started using the new type alias syntax. WPS221
(line complexity) complains about lines that are just type aliases:

```python
type Vector = list[tuple[int, int, str, float, bool]]
```

Running flake8 with wemake-python-styleguide on this gives me a
`LineComplexityViolation` for the line, even though there's no real
logic on it — it's purely a type declaration.

What's weird is that the equivalent old-style form is silently accepted:

```python
Vector: TypeAlias = list[tuple[int, int, str, float, bool]]
```

No WPS221 here. So the same type information, written two different
ways, gets treated very differently by the complexity check.

I'd expect the new PEP695 `type X = ...` syntax to be handled the
same way as the annotated alias — type aliases are essentially type
annotations and shouldn't be inflating line complexity scores.
