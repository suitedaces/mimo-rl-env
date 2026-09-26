[New Rule] Use comparision directly instead of bool(comparison)
## Explanation

Comparisons return boolean values. No need to wrap it in a bool-call

## Example

```python
# Bad
bool(a == b)

# Good
a == b
```
