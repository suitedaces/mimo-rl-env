## A streaming helper for parsing logs line-by-line?

I'm using `grok` in a small log-processing tool. The typical thing I want to do is: open a log file (or read from stdin / a network stream), apply one grok pattern to every line, and hand each parsed result off to my own processing code.

Today the only entry point I see for that is `Parse(pattern, text)`, so every call site of mine ends up looking like:

```go
g, _ := grok.New()

file, _ := os.Open("app.log")
defer file.Close()

scanner := bufio.NewScanner(file)
for scanner.Scan() {
    values, err := g.Parse("%{COMMONAPACHELOG}", scanner.Text())
    if err != nil {
        return err
    }
    // ... do something with values ...
}
```

Two things bother me about this:

1. For a library that's pretty much *aimed* at log parsing, the read-loop boilerplate feels like something the package itself should expose. I'd much rather hand `grok` a reader, a pattern, and a per-line callback, and let it drive the iteration. That way the common "parse this whole stream with this one pattern" case is one call instead of ten lines I copy at every site.

2. When I do this against a real log file (tens of thousands of lines) it feels like the same pattern is being prepared from scratch on every iteration — the pattern string is the same on every line, but I don't have a way to express that to the API; I just keep calling `Parse(pattern, line)` and trust the library. For a streaming use case it would be nice if reusing the same pattern across many lines didn't redo the per-call work each time.

Would you consider adding a stream-oriented parse entry point that covers this use case? The shape I have in mind from a caller perspective is just: "here is something I can read lines from, here is the pattern, here is what to do with each parsed line, please go." Something like a `ParseStream` method on `*Grok` taking a `*bufio.Reader` would fit perfectly.
