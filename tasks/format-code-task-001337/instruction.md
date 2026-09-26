### Glob with a literal (non-wildcard) path returns no directory dependency when the file is missing

I'm using `pathtools.Glob` in some build logic where I sometimes reference a concrete file path (no `*`, `?`, `[`), e.g. `some/dir/generated.go`. The return is `(matches, dirs, err)` and the second value is what I rely on so the build system knows "watch these directories; if anything in them changes, re-evaluate this glob".

This works fine when the file exists, and it works fine for patterns that contain wildcards (e.g. `some/dir/*.go`) regardless of whether anything matches. But for the **literal-path + file-doesn't-exist-yet** case, the behavior seems wrong:

```go
// some/dir exists, but some/dir/generated.go does NOT exist yet
matches, dirs, err := pathtools.Glob("some/dir/generated.go")
// matches: []   (expected — file isn't there)
// dirs:    []   (this is the problem)
// err:     nil
```

`dirs` comes back empty. That means nothing upstream is recorded as a dependency, and when I later actually create `some/dir/generated.go`, there's no signal that this glob's result might have changed — it gets treated as if the glob has no inputs at all.

Compare that with the wildcard case:

```go
// same situation, but with a wildcard
matches, dirs, err := pathtools.Glob("some/dir/*.go")
// dirs includes some/dir, so creating a new .go file there is noticed
```

I'd expect a literal pattern to behave similarly w.r.t. dependency tracking: even if the exact file isn't present right now, the glob should still report enough directory information for the caller to notice when that file (or some ancestor on the way to it) appears later. Right now there's literally nothing to hang a "rerun me when this changes" hook on.

This also matters when the immediate parent doesn't exist either — e.g. globbing `a/b/c/d.txt` where only `a/` currently exists. Today that returns `(nil, nil, nil)` and you're stuck.

Could `Glob` / `GlobWithExcludes` be fixed so that the literal-pattern-with-missing-file case still produces a usable `dirs` result?
