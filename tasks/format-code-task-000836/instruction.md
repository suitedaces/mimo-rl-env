## `$$` is not treated as an escaped dollar sign

When using envsubst to expand variables in templates (e.g. shell scripts or docker-compose-style files), there's no way to put a literal `$` in the output. The conventional escape — doubling it as `$$` — isn't recognized.

For example:

```go
out, _ := envsubst.EvalEnv("price is $$5")
// want: "price is $5"
```

or in a more typical case where I want a literal `$` next to a word that looks like a variable name:

```go
os.Setenv("var", "hello")
out, _ := envsubst.EvalEnv("$$var")
// want: "$var"
```

Neither of these produces the expected output. This is the same convention used by `docker-compose` and `make`, so it would be nice for envsubst to support it too.
