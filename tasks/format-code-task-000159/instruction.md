[New Rule] Simplify "in dict.keys()" to "in dict"
## Explanation

Most of the discussion of the motivation about this rule can be found in this very detailed [StackOverflow post](https://stackoverflow.com/a/29314342)

## Example

```python
# Bad
key in dict.keys()

# Good
key in dict
```

Basically, the later way of doing this pythonic and slightly more performant and arguably more Readable. The previous method only exists for legacy code (<= python 2.2). So there is no reason to use the former in modern codebases.
