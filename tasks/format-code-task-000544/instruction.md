# Make the Java output normalizer cope with all our stack-trace shapes

Our test harness compares the output of transpiled programs run on the JVM against
expected output. Because raw JVM output is noisy (full Java stack traces, native
memory addresses, `E`-style float exponents), the harness first runs everything
through `cleanse_java(output)` in the test utilities, which collapses a Java
exception into a stable, canonical block before comparison.

`cleanse_java` currently only understands a couple of trace layouts, and it
mishandles others — for some traces the exception name and message come out
empty, and newer runner setups emit traces it doesn't recognise at all. Make it
robust to every shape of exception output we actually see.

## Canonical form

When the input contains an `org.python.exceptions.*` exception, the whole
exception region must be replaced with:

```
### EXCEPTION ###
<Name>: <message>
    <file>:<line>
    ...
```

- `<Name>` is the exception class with the leading `org.python.exceptions.`
  package stripped (e.g. `org.python.exceptions.KeyError` → `KeyError`).
- `<message>` is the text following the exception class on that line, verbatim.
- One indented `    <file>:<line>` line follows per stack frame, but only for
  frames in the transpiled program's own classes (those whose class path begins
  with `python.`), and frames for synthesised Java constructors (the
  `.<init>` frames) are dropped. The frames are listed outermost-first — i.e.
  the reverse of the order they appear in the raw trace.
- Any program output printed before the exception is preserved unchanged, and
  unrelated normalizations the helper already performs (masking memory addresses
  like `0x1eb19f4e` to `0xXXXXXXXX`, and lowercasing float exponents such as
  `7.95E-6` → `7.95e-6`) must keep working.

## Trace shapes that must be handled

1. **Direct exceptions**, where the first line is the exception itself:
   `org.python.exceptions.SomeError: message`, followed by `at ...` frames.

2. **Wrapped exceptions**, where a Java wrapper (e.g.
   `java.lang.ExceptionInInitializerError`) is reported first, optionally
   followed by some reflection `at ...` frames, then a
   `Caused by: org.python.exceptions.SomeError: message` line and its `at ...`
   frames. The trailing `... N more` continuation line that the JVM appends to a
   "caused by" trace must not leak into the output.

In both shapes the leading `Exception in thread "<thread>"` label is optional
(some environments omit it), and the thread name may contain hyphens. The
exception name, message, and the selected file/line frames must be reported
correctly regardless of which shape and whether the label is present.
