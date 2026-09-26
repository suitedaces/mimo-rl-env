<new-for-builtins> : potential side effects auto fix
This is more of a question than actual bug report.

`new-for-builtins` autofixes this code:

```js
const str = new String('test')
```

to this:
```js
const str = String('test')
```

The problem is that 2 values are not identical.
For example:

```js
String('test') === String('test') // true
new String('test') === new String('test') // false
```

Is this intended behavior?

The rule was first implemented in #105
