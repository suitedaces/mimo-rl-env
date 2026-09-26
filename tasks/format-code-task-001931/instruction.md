## `global_defs` rewrites the left-hand side of an assignment, producing invalid output

I'm using `global_defs` as a build-time flag, similar to how `DefinePlugin` works in webpack:

```js
var result = UglifyJS.minify("input.js", {
    compress: {
        global_defs: { DEBUG: false }
    }
});
```

My source has a place where the same name appears on the left of an assignment (it's a writable flag, e.g. set once during bootstrap):

```js
DEBUG = true;
if (DEBUG) { console.log("hi"); }
```

After minifying, the output contains something like:

```js
false = true; ...
```

which obviously blows up the moment the browser tries to run it. The `if (DEBUG)` site getting replaced with `false` is fine and what I want; the assignment site is not — you can't assign to a literal.

I'd expect `global_defs` to substitute only where the name is *read*, not where it's being written to. The current behavior makes `global_defs` unusable for any name that ever appears on the LHS of an `=` in the source, even though the assignment itself is dead code after the substitution propagates.
