## `doctest_module(..., 'all')` stops at the first failure instead of running the whole batch

I'm using xdoctest to run all the doctests inside one of my modules:

```python
from xdoctest import doctest_module
doctest_module('mypkg.mymod', 'all')
```

The module has ~10 doctests. As soon as one of the earlier ones fails, the
runner raises out of `_run_examples` and the rest of the doctests are never
executed. So I see exactly one traceback, no summary, no idea which of the
remaining tests pass or fail. To find out, I have to fix that one test and
re-run the whole batch, hit the next failure, fix, re-run, etc.

What I'd expect from an "all" run is the usual test-runner behavior: keep
going on failure, run every collected example, and at the end print the
failures along with a "N / M passed" summary so I can see the whole picture
in one pass. Failing fast still makes sense when there's only a single
example being run (e.g. when I'm debugging one specific doctest by name) —
in that case I do want the exception to propagate so I get the traceback
immediately.

---

While poking at this I also noticed `doctest_module`'s `argv` parameter
doesn't really behave like one would expect. Two things:

1. Passing `argv=['--verbose']` (or `argv=['all', '--quiet']`, etc.) from
   Python doesn't change the verbosity / style. The flags I put in `argv`
   are ignored and it looks at the real process `sys.argv` instead. That
   makes it hard to drive xdoctest programmatically from another script /
   test harness where I don't want to mutate `sys.argv`.

2. If the first entry of `argv` is a flag (e.g. `argv=['--verbose']` with
   no explicit command), it ends up being treated as the test name to run
   and of course matches nothing. I'd expect flags to be recognized as
   flags regardless of position, and the command to default to "no command
   given" in that case.

Both feel like the `argv` handling should consistently use the argv that
was passed in.
