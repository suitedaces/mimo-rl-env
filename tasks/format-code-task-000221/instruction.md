## baron doesn't recognize PEP 515 underscores in numeric literals

I'm using `baron` to parse and analyze Python source code in a project that targets Python 3.6+. Since [PEP 515](https://peps.python.org/pep-0515/) (accepted in 3.6), it's legal to use single underscores as visual separators inside numeric literals, and this style shows up all over modern codebases — readability for large constants, bitmasks, etc.

baron doesn't seem to know about this syntax.

### Reproducer

```python
import baron

src = "x = 1_000_000\n"
print(baron.dumps(baron.parse(src)))
```

Anything similar fails the same way:

```python
total      = 1_000_000
mask       = 0xFF_FF_FF_FF
flags      = 0b1010_1010
perms      = 0o755_000
ratio      = 1_000.5
```

All of these are valid Python 3.6+ and CPython tokenizes each one as a single numeric literal. baron either errors out or splits the literal apart at the underscore (so `1_000_000` does not come back as a single number token the way `1000000` does), which makes the resulting tree unusable for anything that has to round-trip the source.

### Expected

baron's tokenizer should accept underscore separators in numeric literals consistently with what CPython 3.6+ accepts — integers, floats, hex, octal and binary literals (and the corresponding `L`-suffixed long variants that baron already supports for Python 2). Effectively the same code that parses today without the underscores should parse identically when underscores are inserted between digits.
