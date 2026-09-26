Support the post-rewrite hook type
It would be useful to me for pre-commit to support the `post-rewrite` hook:

https://git-scm.com/docs/githooks

> post-rewrite
This hook is invoked by commands that rewrite commits (git-commit[1] when called with --amend and git-rebase[1]; however, full-history (re)writing tools like git-fast-import[1] or git-filter-repo typically do not call it!). Its first argument denotes the command it was invoked by: currently one of amend or rebase. Further command-dependent arguments may be passed in the future.

My use-case is automatically running `poetry install` for a project when merging, rebasing, or checking out a different branch.  Most of this is possible with the `post-checkout` and `post-merge` hooks, but when rebasing a branch the `post-merge` hook is run before the rebasing applies changes of my branch.

For example:

```
 $ git pull origin main
remote: Enumerating objects: 11, done.
remote: Counting objects: 100% (11/11), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 11 (delta 4), reused 11 (delta 4), pack-reused 0
Unpacking objects: 100% (11/11), 31.67 KiB | 5.28 MiB/s, done.
From REDACTED
 * branch            main       -> FETCH_HEAD
   9a12988..36da943  main       -> origin/main
First, rewinding head to replay your work on top of it...

###
### The pre-commit hook runs here
###

Install dependencies.....................................................Passed
- hook id: poetry install
- duration: 2.83s
Installing dependencies from lock file
Package operations: 0 installs, 2 updates, 0 removals
  • Updating pytest (6.2.4 -> 6.2.5)
  • Updating pre-commit (2.14.0 -> 2.14.1)
Installing the current project: REDACTED (0.0.1)
Install pre-commit hooks.................................................Passed
- hook id: pre-commit install
- duration: 0.45s
Applying: REDACTED
Applying: REDACTED

###
### I would like the pre-commit hook to run here
###
```
