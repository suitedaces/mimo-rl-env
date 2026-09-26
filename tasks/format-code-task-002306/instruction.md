## Jenkins pipeline files can't be targeted as a distinct type

I'm setting up `pre-commit` for a CI-heavy repo that runs on Jenkins.
We've got a `Jenkinsfile` at the repo root, and a few shared pipeline
snippets named `*.jenkins` under `ci/`.

I want to run a Jenkins-specific linter against just these pipeline
files (and not against every random Groovy script in the tree). When
I check what `identify` actually returns for these paths:

- `Jenkinsfile` → comes back as `text` + `groovy`
- something like `ci/deploy.jenkins` → not picked up as anything specific

This makes it impossible to write a pre-commit hook filter that runs
only on Jenkins pipeline files: filtering on `groovy` is too broad
(it would also fire on plain `.groovy` source files in the repo,
which I don't want a Jenkins linter touching), and there's no other
tag I can use to single out the pipeline files. And the `.jenkins`
extension — which is a fairly common convention for Jenkins shared
library / pipeline template files — doesn't seem to be on identify's
radar at all.

Could `identify` recognize Jenkins pipeline files as their own type,
so they can be targeted independently of generic Groovy code? Ideally
both `Jenkinsfile` (the well-known root file) and `*.jenkins` (the
extension a lot of teams use for pipeline scripts) would be covered.
A dedicated tag like `jenkins` (alongside the existing `text` / `groovy`
tags) would do the trick, and ideally `*.jenkinsfile` would be treated
the same way too.
