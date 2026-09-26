`extendEnv` does not work when combined with `shell: true`
The `extendEnv` option does not work as intended when combined with the `shell: true` option:

```js
process.env.TEST = 'test'
const result = execa.sync('echo $TEST', { shell: true, env: {}, extendEnv: true })
assert.equal(result.stdout, 'test')
```

`stdout` is an empty string but should be `'test'`

I will work on a PR to fix this.
