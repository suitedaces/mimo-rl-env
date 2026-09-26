Export statement using babel-plugin-transform-export-extensions syntax introduces semantic change
```js
export foo, {bar} from './baz';
```

is turned into 
```js
export { foo, bar } from "./baz";
```


Repro:
https://prettier.github.io/prettier/#%7B%22content%22%3A%22export%20foo%2C%20%7Bbar%7D%20from%20'.%2Fbaz'%3B%5Cn%22%2C%22options%22%3A%7B%22printWidth%22%3A80%2C%22tabWidth%22%3A2%2C%22singleQuote%22%3Afalse%2C%22trailingComma%22%3A%22%22%2C%22bracketSpacing%22%3Atrue%2C%22jsxBracketSameLine%22%3Afalse%2C%22parser%22%3A%22%22%2C%22doc%22%3Afalse%7D%7D
