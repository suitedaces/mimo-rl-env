prettier transforms a [Flow declaration](https://flowtype.org/docs/declarations.html) like

```js
declare type Foo = string;
```

into

```js
type Foo = string;
```

Here's [that in the web UI](https://jlongster.github.io/prettier/#%7B%22content%22%3A%22declare%20type%20Foo%20%3D%20string%3B%22%2C%22options%22%3A%7B%22printWidth%22%3A80%2C%22tabWidth%22%3A2%2C%22singleQuote%22%3Afalse%2C%22trailingComma%22%3Afalse%2C%22bracketSpacing%22%3Atrue%2C%22doc%22%3Afalse%7D%7D).

Are flow declarations in scope for prettier or are they not considered proper JavaScript?
