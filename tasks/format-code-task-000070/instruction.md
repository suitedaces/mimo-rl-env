## Manage the `orchestrion.tool.go` file incrementally

`orchestrion pin` records which tracer integrations are enabled in a module by
maintaining a build-tagged Go source file named `orchestrion.tool.go`. Today
that file is rewritten from scratch on every run, which throws away anything a
user added by hand. We want to manage it incrementally instead.

Add a small, reusable piece of functionality (in package
`github.com/DataDog/orchestrion/internal/pin/toolfile`) that creates or refreshes
this file for a given module directory. It should expose:

```go
type Options struct {
    NoGenerate bool
}

func Update(dir string, opts Options) error
```

`Update` operates on `<dir>/orchestrion.tool.go` and must behave as follows:

- **Creation.** When the file does not exist, create it as a valid Go source
  file carrying a `//go:build tools` build constraint, declared in
  `package tools`, and containing a blank import (`_ "..."`) of
  `github.com/DataDog/orchestrion`.

- **Incremental update.** When the file already exists, parse it and keep every
  import it already declares — including blank imports a user added manually —
  while ensuring the blank import of `github.com/DataDog/orchestrion` is present.
  Each imported package must appear exactly once (no duplicates), and the result
  must remain a valid Go source file in `package tools` with the
  `//go:build tools` constraint.

- **Generate directive.** Unless `Options.NoGenerate` is set, the file must
  contain a `//go:generate go run github.com/DataDog/orchestrion pin` directive.
  When `NoGenerate` is true, the directive must not be present — and if it was
  there before, it must be removed.

- **Idempotency.** Running `Update` repeatedly with the same options must
  converge to a stable result: a second invocation leaves the file byte-for-byte
  identical to the first.

- **Bad input.** If the file exists but cannot be parsed as Go source, `Update`
  must return an error and leave the file untouched.
