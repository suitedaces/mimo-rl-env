## `idx()` inside an `async` function throws "must be an arrow function"

I'm using `babel-plugin-idx` together with `babel-preset-env` in my build. With the browser targets I care about, `preset-env` ends up downcompiling `async`/`await`.

As soon as I put an `idx` call inside an `async` function, the build blows up. A minimal repro of what I'm doing:

```js
async function loadStuff(props) {
  return idx(props, _ => _.user.profile.name);
}
```

I get:

```
The second argument supplied to `idx` must be an arrow function.
```

…which is confusing because the second argument *is* an arrow function — I literally just wrote it. And the exact same `idx(...)` call transforms just fine if I lift it out of the `async` function into a regular function:

```js
function loadStuff(props) {
  return idx(props, _ => _.user.profile.name);   // works
}
```

So whatever the plugin is checking against, only the async wrapper seems to break it.

I'd expect `idx` to work the same way regardless of whether the surrounding function is `async`.
