## `raise` with a non-exception value gives garbage output instead of a TypeError

While running some Python code through Skulpt, I noticed that `raise` doesn't
match CPython's behavior when you give it something that isn't an exception.

Minimal repro:

```python
raise 1
```

In CPython 3 I get the expected behavior:

```
TypeError: exceptions must derive from BaseException
```

But running the same one-liner under Skulpt, I get something like:

```
undefined undefined
```

instead of any kind of meaningful error. Same thing happens if I try
`raise "oops"` or `raise SomeClassThatIsNotAnException` — Skulpt just emits
that `undefined undefined` output rather than telling me I'm not allowed to
raise non-exception values.

According to the Python data model, `raise` is only supposed to accept
instances or subclasses of `BaseException`; anything else should produce a
`TypeError`. It would be great if Skulpt could match CPython here so that
students using Skulpt-based environments see the same error message they'd
see in a "real" Python interpreter (and so that the output is actually
something readable instead of `undefined undefined`).
