"TypeError: next.match is not a function" with "number" values
```js
const parse = require('yargs-parser');

args = parse( ['--p', 2] );
```
Results in:
```
TypeError: next.match is not a function
    at parse (D:\yargs-parser\node_modules\yargs-parser\index.js:193:42)
    at Parser (D:\yargs-parser\node_modules\yargs-parser\index.js:901:16)
```

The opposite - converting `number` into `string` works fine:
```js
args = parse( ['--p', '2'] );         // { _: [], p: 2 }
```
