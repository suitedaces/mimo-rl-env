## Comments above the first import get mangled after sorting

I have a Python file where I put a short `#` comment line directly above an import to explain what it's for. After running `isort` on the file, the comment ends up duplicated / misplaced — it loses its "this comment belongs to that import" relationship.

Minimal example. Input file:

```python
"""Module docstring."""
# Comment explaining the next import
from foo import bar

from baz import qux
```

After `isort file.py`, the output around the top of the file is no longer right — the comment line `# Comment explaining the next import` is not where I'd expect it to be relative to `from foo import bar` anymore. It looks like the breakage is specifically around comments attached to the very first import in the file; if I move the same comment to sit above the *second* import instead, isort handles it fine.

I'd expect isort to preserve a `#` comment that sits directly above an import as a comment belonging to that import, regardless of whether that import happens to be the first one in the file or not. Right now I have to manually clean up the top of every file after running isort, which kind of defeats the point.

Tested on the current `develop` checkout.
