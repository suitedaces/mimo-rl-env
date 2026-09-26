constant-glob fails to lint when the first argument is named
constant-glob does not correctly lint constant globs when using a named `include` parameter.

This raises a warning:
```
❯ echo 'glob(["foo.py"])' | buildifier -lint=warn -warnings=+constant-glob -type build -
glob(["foo.py"])
<stdin>:1: constant-glob: Glob pattern "foo.py" has no wildcard ('*'). Constant patterns can be error-prone, move the file outside the glob. (https://github.com/bazelbuild/buildtools/blob/master/WARNINGS.md#constant-glob)
```

This fails to raise a warning, even though I'd expect it to:
```
❯ echo 'glob(include = ["foo.py"])' | buildifier -lint=warn -warnings=+constant-glob -type build -
glob(include = ["foo.py"])
```
