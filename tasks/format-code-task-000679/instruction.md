`gh release create`: "Write using git tag message as template" option is hidden sometimes even when annotations exist
### Describe the bug

`gh --version`:
gh version 2.4.0 (2021-12-21)
https://github.com/cli/cli/releases/tag/v2.4.0

In earlier versions, I would *always* see the option to create release notes from a tag message if the tag was annotated. Currently, that option is hidden when I own the repository.

### Steps to reproduce the behavior

```shell
gh repo clone me/my-repo
cd my-repo
git tag -am "foo" bar
gh release create bar # don't see option
```
```shell
gh repo clone another-user/repo-i-do-no-maintain
cd repo-i-do-not-maintain
git tag -am "foo" bar
gh release create bar # see tag message option
```

### Expected vs actual behavior

I expect the "Write using git tag message as template" option to *always* appear, assuming the annotated tag is available.

### Extra Info

I think these lines are doing it. It looks like, as long as `generatedNotes != nil`, `tagDescription` is not set, so it equals `""`.
https://github.com/cli/cli/blob/ad8d7bb02e36e66e28c78837f5392afd1a5187a3/pkg/cmd/release/create/create.go#L237-L239
https://github.com/cli/cli/blob/ad8d7bb02e36e66e28c78837f5392afd1a5187a3/pkg/cmd/release/create/create.go#L261-L263
