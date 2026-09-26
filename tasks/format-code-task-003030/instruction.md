odd behavior of narg:2 versus duplicate-arguments-array:false
```
const P = require('yargs-parser')
P('foo -p x y', { narg: { p: 2 } })
{ _: [ 'foo' ], p: [ 'x', 'y' ] }
```

i.e. this results in the expected `{x:'y'}` binding.

whereas:
```
P('foo -p x y', { narg: { p: 2 }, configuration: {  'duplicate-arguments-array': false } })
{ _: [ 'foo' ], p: 'y' }
```

which seems buggy, and contrary to the documentation. i would expect the resulting binding to be the same in both cases.
