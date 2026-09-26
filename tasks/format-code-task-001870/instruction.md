optimize representation of empty lines in `<li>` and `<blockquote>` content
In `<li>`, empty lines still get indenting spaces (spaces replaced with `·` in output):

```python
from markdownify import markdownify as md

html = """
<ul>
  <li>
    <p>1</p>
    <p>2</p>
  </li>
</ul>
"""
print(md(html))
# *·1
# ·· <-- HERE
# ··2
```

Similarly in `<blockquote>` empty lines get trailing marker spaces:

```python
from markdownify import markdownify as md

html = """
<blockquote>
  <p>1</p>
  <p>2</p>
</blockquote>
"""
print(md(html))
# >·1
# >· <-- HERE
# >·2
```

These empty spaces are unnecessary and can be omitted for brevity.
