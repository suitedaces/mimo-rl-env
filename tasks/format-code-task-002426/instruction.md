## `imp.load_source()` breaks with hash-based .pyc files

I'm maintaining some older code that still uses `imp.load_source()` to pull in a Python file by path. It used to work fine, but after switching to hash-based bytecode caches (PEP 552) on 3.7, it blows up during the load.

Minimal repro:

```python
import imp
mod = imp.load_source('mymod', '/path/to/mymod.py')
```

With a regular (timestamp-based) pyc cache this is fine. With hash-based pycs enabled, the call fails partway through while the cache is being written.

Direct `importlib` loading of the same file works without issue — only the `imp.load_source` path is affected, so this looks like a compatibility gap in the `imp` shim rather than a problem with the source file itself.

`imp` is deprecated, I know, but it's still documented and there's a fair amount of legacy code (mine included) calling `load_source`. It would be nice if it kept working on 3.7+ regardless of which pyc format is in effect.
