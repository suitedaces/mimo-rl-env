Error when using window as a prop
**Do you want to request a *feature* or report a *bug*?**

A bug.

**What is the current behavior?**

One third party React component I'm using use `window` as a prop. When trying to snapshot test it, I'm getting the following error:

```js
RangeError: Invalid string length

      at Object.test (src/SelectField.test.js:17:52)
          at Promise (<anonymous>)
          at <anonymous>
      at process._tickCallback (internal/process/next_tick.js:188:7)
```

I'm guessing this is an issue with `pretty-format` as the same error can be reproduced when trying to pretty format `window`:

```js
test('something', () => {
  const windowRepresentation = prettyFormat(window)
});
```

This would lead to a similar error:

```js
RangeError: Invalid string length

  at printListItems (node_modules/pretty-format/build/collections.js:174:256)
  at Object.<anonymous>.test (index.test.js:4:32)
      at Promise (<anonymous>)
      at <anonymous>
  at process._tickCallback (internal/process/next_tick.js:188:7)
```

I've setup a [small repro](https://github.com/HiDeoo/jest-repro) leading to this exact same error when trying to pretty format `window`.

- `jest` version: 21.2.1
- `node` version: 8.4.0
- `yarn` version: 1.1.0
