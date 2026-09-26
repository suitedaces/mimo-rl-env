### Astro Info

```block
Astro                    v4.2.6
Node                     v18.18.0
System                   Linux (x64)
Package Manager          unknown
Output                   static
Adapter                  none
Integrations             none
```


### If this issue only occurs in one browser, which browser is a problem?

_No response_

### Describe the Bug

In the build output, astro seems to ignore `trailingSlash: 'never'` and `Astro.url` always creates URLs with a trailing slash.

Go to the Stackblitz reproduction and build the project with `npm run build`. Then check the generated html file at `./dist/subpath/index.html`. The canonical link has a trailing slash.

### What's the expected result?

`trailingSlash: 'never'` should be considered for `Astro.url`.

### Link to Minimal Reproducible Example

https://stackblitz.com/edit/github-gs5j67?file=src%2Fpages%2Fsubpath.astro,astro.config.mjs%3AL7

### Participation

- [ ] I am willing to submit a pull request for this issue.
