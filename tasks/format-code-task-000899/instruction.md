## Logs disappear silently when using `AddTestScope`

I'm writing a devstack test and using `devtest.AddTestScope(ctx, "...")` to tag log lines with a test scope. After adding the scope, log calls that go through the resulting context simply produce no output — the lines I'd expect to see in the test output are just missing. There's no panic, no error printed, nothing in stderr, the test just runs and the log calls behave as if they were no-ops.

Rough shape of what I'm doing:

```go
ctx := devtest.AddTestScope(t.Ctx(), "my-subtest")
logger := /* the op-service logger configured with the context handler */
logger.InfoContext(ctx, "starting step", "foo", "bar")  // <- never appears
```

If I skip `AddTestScope` entirely the same log line shows up fine, so something about the scope-tagged context is making the log get dropped on the floor.

This is pretty painful to debug because there's zero signal that anything went wrong — you just stare at empty output and wonder whether the log call ran at all. Two things I'd like to see fixed:

1. `AddTestScope` should work — adding a test scope to the context shouldn't cause subsequent log calls on that context to vanish.
2. More generally, if something is wrong with the values that the context handler is trying to attach to a log record, that shouldn't silently drop the entire log line. A developer should at least get *some* visible indication that things aren't working, instead of having logs disappear without a trace.
