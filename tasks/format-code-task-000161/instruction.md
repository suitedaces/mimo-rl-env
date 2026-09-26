[SIM905] Use list of strings instead of splitting a constant string
## Explanation

You want a list of strings? Create one directly:

* A list of strings can be formatted by black.
* Your editor can sort the lines
* You don't have to worry about how to keep leading / intermediate / trailing spaces or how to add newlines to the strings


## Example

```python
# Bad
domains = "de com net org".split()

# Good
domains = ["de", "com", "net", "org"]
```
