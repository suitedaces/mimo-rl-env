### `oc import-image` gives a useless error when the tag doesn't exist on the image stream

I have an image stream where each tag is defined individually under `.spec.tags` (no top-level `.spec.dockerImageRepository`). I wanted to refresh a single tag, but I mistyped the tag name:

```
$ oc import-image myapp:v3
error: unexpected error, from is empty
```

`v3` isn't actually a tag on `myapp` — I meant `v2`. So the import legitimately can't proceed. But the message I get back is completely opaque; it reads like an internal assertion failure rather than something I did wrong, and it doesn't tell me what to do next.

It would be much friendlier if `import-image` recognized that I'm asking it to import a tag that doesn't exist on the image stream and told me so — ideally also pointing me at the right command for actually creating a new tag (so I don't sit there wondering whether `--confirm` or `--from` would have helped). Right now there's nothing in the output that suggests `oc tag` is the thing I should reach for.

Bug: https://bugzilla.redhat.com/show_bug.cgi?id=1318537
