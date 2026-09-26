## `%+v` on errtrace-wrapped errors doesn't include the return trace

I'm using errtrace to track how errors propagate through my service, and
I log errors at the top of my handlers the same way I would with most
other error libraries:

```go
if err := doWork(ctx); err != nil {
    log.Printf("request failed: %+v", err)
    return
}
```

`doWork` and everything it calls wraps returned errors with
`errtrace.Wrap`, so by the time the error reaches my handler it already
carries a full return trace internally.

The problem: the `%+v` output looks identical to plain `%v` — I just get
the underlying error's message on a single line, with no trace at all.
To actually see the return path I have to remember to call
`errtrace.Format(os.Stderr, err)` (or `errtrace.FormatString(err)`) as a
separate step, which is easy to forget and clutters every error-logging
site.

I'd expect that when I format an errtrace-wrapped error with `%+v`, the
return trace comes along automatically — that's the whole reason I
reached for errtrace over plain `fmt.Errorf`. The other common verbs
(`%v`, `%s`, `%q`, ...) should still behave the way they do today so
existing logs don't suddenly change shape; only `%+v` needs to opt into
the richer output.

Could errtrace render the trace itself when the caller asks for the
verbose form, instead of requiring a separate `Format` call?
