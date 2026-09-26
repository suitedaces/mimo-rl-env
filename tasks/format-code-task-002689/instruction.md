## Appending `?subtree=true` to file/dir URLs breaks when the URL already has query params

We construct links to files and directories in a few places (the file-match results list, `RepoFileLink`, and the "go to dir"/"go to file" search suggestions) by string-concatenating `?subtree=true` onto a URL, roughly:

```tsx
<Link to={`${fileURL}?subtree=true`}>...</Link>
```

This silently assumes `fileURL` never already contains a query string. That assumption is about to stop holding: we're getting ready to land version contexts, which will mean URLs can legitimately arrive at these call sites already carrying a query param (e.g. something like `/github.com/foo/bar/-/blob/baz.go?someParam=x`). With the current code those would become `/github.com/foo/bar/-/blob/baz.go?someParam=x?subtree=true` — two `?` in the same URL, which is just wrong and will break navigation / linking.

This isn't a one-off either; we have several call sites all doing the same `${url}?subtree=true` pattern, so the bug is duplicated and will keep getting reintroduced as long as everyone hand-rolls the concatenation.

Could we fix the way `subtree=true` is appended so that it merges cleanly when the URL already has other query params, and ideally route all the existing call sites through one shared helper so this doesn't regress later? The places I know of off the top of my head are the search file-match children, `RepoFileLink`, and the file/dir entries built in the search suggestion list, but it'd be good to audit for any others.

The shared helper I'd expect to add lives in `shared/src/util/url.ts` and would be something like `appendSubtreeQueryParam(url)`.
