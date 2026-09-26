Can't reimplement MustParse behaviour when using NewParser
`MustParse` is really helpful: https://github.com/alexflint/go-arg/blob/74af96c6ccf404613c251bca4814d32c69047c5f/parse.go#L85-L95

However, if you want to use a custom `Config`, you have to call `NewParser()` which returns a `*Parser` but hasn't gone through the steps `MustParse` takes. Though I can implement most of `MustParse` myself again by calling `parser.Parse(os.Args)` first and then switching on the resulting `err` like `MustParse` does and calling the exported `WriteHelpForSubcommand()` and `FailWithSubcommand()`.

I can't access `version` and `lastCmd` since those are unexported and there doesn't appear to be an exported equivalent. Version I can still get to using something like `&args.Version()` or having a `func Version()`, but `lastCmd` appears completely unaccessible.
