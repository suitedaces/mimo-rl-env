# Allow a plain function to be used as an assertion

Right now the only things you can pass as the second argument to `expect` are an
assertion string (`expect(2, 'to be a number')`) or an `expect.it(...)`
expression. If you pass a bare function instead, you get an error:

```
The expect function requires the second parameter to be a string or an expect.it.
```

That's annoying, because a function is the most natural way to express an ad-hoc
check. Please make a plain function a first-class assertion argument.

When the second argument to `expect` is a function, it should be treated as an
inline assertion: call the function once, passing the subject as its only
argument.

- If the function returns without throwing, the expectation succeeds.
- If the function throws, the expectation fails with that error.
- Asynchronous checks must work too: if the function returns a promise, the
  expectation should adopt it — a fulfilled promise means success, and a
  rejected promise means the expectation fails (rejects) with that same error.

This has to work in both places an assertion can be run:

- at the top level — `expect(subject, fn)`; and
- from inside a custom assertion's implementation, where calling
  `expect(subject, fn)` should behave like any other nested assertion: on
  failure the function's error is reported nested within the surrounding
  assertion's output rather than replacing it.

Passing a function must no longer raise the "second parameter" error described
above.

Everything that already works must keep working unchanged: string assertions,
and `expect.it(...)` expressions (which are themselves functions) used as the
second argument.
