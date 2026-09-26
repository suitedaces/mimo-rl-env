## Require space between keyword and opening parenthesis

I keep running into Python code that uses keywords as if they were functions:

```python
def func():
    a = 1
    b = 2
    del(a, b)
    return(a)

def gen():
    yield(1, 2, 3)
```

This is syntactically valid, but `return`, `yield`, `del`, `assert`, `not`, etc. are *keywords*, not function calls. Writing them with no space before the `(` makes them look like functions — which is exactly the confusion `print` caused back in Python 2 vs 3, and it still trips people up when reading the code.

It would be great if wemake-python-styleguide could flag this under the consistency rules and require a space between a keyword and a following `(`, so the examples above would be rewritten as:

```python
def func():
    a = 1
    b = 2
    del (a, b)
    return (a)

def gen():
    yield (1, 2, 3)
```

This way it's visually obvious that the thing on the left is a keyword, not a callable.

Following this project's convention I'd expect a new token visitor (something like a `WrongKeywordTokenVisitor`) raising a new consistency violation along the lines of `MissingSpaceBetweenKeywordAndParenViolation`.
