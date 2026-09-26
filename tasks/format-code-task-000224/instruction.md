## D300 doesn't catch docstrings that start with too many quotes

I run `pydocstyle` over my codebase to enforce PEP 257. While reviewing some code today I noticed I had typoed a docstring like this:

```python
def my_function():
    """"Compute something useful."""
    pass
```

Notice the **four** opening `"` instead of three — a typo. This is still valid Python (the parser just treats the 4th `"` as the first character of the docstring body), but it's clearly not what I wanted, and any human reader would call it a mistake.

I expected D300 ("Use \"\"\"triple double quotes\"\"\"") to flag this, since the opening quoting is plainly wrong. But pydocstyle reports no error at all on this file. The same is true for things like:

```python
def another():
    '''''Whatever.'''''
    pass
```

— extra leading quotes go completely unreported.

Could D300 be extended to catch the case where a docstring begins with superfluous opening quotes? Right now it seems to only check that the opening is some form of triple-quote-with-optional-prefix, and any "extra" quotes on the front silently slip through, which defeats the point of the check for these typo-style mistakes.
