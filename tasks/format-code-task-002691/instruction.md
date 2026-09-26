## Move `CommitExists` / `Head` into `internal/vcs/git`, drop the stderr-string matching

Right now the only implementation of "does this commit exist?" lives on the codeintel gitserver `Client` in `enterprise/internal/codeintel/gitserver/client.go`. The way it decides whether a commit exists is:

```go
out, err := c.execGitCommand(ctx, repositoryID, "cat-file", "-t", commit)
if err == nil {
    return true, nil
}

if strings.Contains(out, "Not a valid object name") {
    err = nil
}
return false, err
```

i.e. it shells out to `git cat-file -t`, and if that fails it scans the output for the literal string `"Not a valid object name"` to decide between "commit really doesn't exist" and "something else went wrong". That's fragile — any wording change from git (or any wrapping layer that doesn't propagate stderr verbatim) and we silently start reporting genuinely-missing commits as errors, or vice versa. We already have a perfectly good typed signal for this case (`gitdomain.RevisionNotFoundError`) elsewhere in the codebase; commit-existence checks should be using that, not regexing English error messages.

Same story for `Client.Head` — it's just `rev-parse HEAD` plus the "no HEAD ⇒ (empty, false, nil)" convention, and there's nothing codeintel-specific about it, but it's only reachable through the codeintel client today. If anything outside codeintel wants either of these, it has to either depend on the codeintel package or reimplement them.

These two operations are repository-generic and belong in `internal/vcs/git` alongside the rest of the commit helpers (`GetCommit`, `Commits`, `FirstEverCommit`, …). I'd like to:

1. Have `internal/vcs/git` expose a "commit exists" check and a "get HEAD" helper that other packages can call directly, given a repo name + commit id.
2. The "commit exists" one should use the typed `RevisionNotFoundError` path to distinguish "missing" from "actual error" — no more stderr string matching.
3. The "get HEAD" one should keep the existing behavior on empty/HEAD-less repos: return an empty revision with a false-valued "exists" flag and a nil error, instead of surfacing the missing-revision error to callers.
4. Once those exist, the codeintel `Client.CommitExists` / `Client.Head` should just resolve the repository id to a repo name and delegate, so the fragile implementations go away.
