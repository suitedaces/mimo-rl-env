### Describe the bug

Using `gh` to `browse` a file with given line number does not work with Markdown files. The URL the user is taken to is the rendered Markdown view without line numbers on the left-hand side.

### Steps to reproduce the behavior

```
$ gh browse README.md:3
now opening https://github.com/cli/cli/tree/trunk/README.md#L3 in browser
$ gh --version
gh version 2.0.0 (2021-08-24)
https://github.com/cli/cli/releases/tag/v2.0.0
```

### Expected vs actual behavior

Looks like a `?plain=1` parameter was [added to GitHub Web UI](https://github.blog/changelog/2021-06-30-parameter-to-disable-markdown-rendering/) to specifically help navigate to Markdown lines.

So, instead of:
* https://github.com/cli/cli/tree/trunk/README.md#L3

I'd expect the user to be taken to:
* https://github.com/cli/cli/blob/trunk/README.md?plain=1#L3

_note: the new URL has `blob` in the path because `?plain=1` does not work with `tree` in the path_

### Logs

N/A
