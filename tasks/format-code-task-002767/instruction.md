Better error output for --report-needless-disables
> What is the problem you're trying to solve?

`--report-needless-disables` current returns error like this:

```
assets/foo.css
start: 2
```

This message is very unclear. Imagine going into a new project trying to contribute, and get  this message by running `npm run lint`.

Currently the developer would have to go read exactly what the lint command executes, and figure out which one of those command created this output, and then work out what `start` means.

> What solution would you like to see?

Something as simple as:

```
assets/foo.css
unused rule: color-named, start line: 2
```

would help a lot.
