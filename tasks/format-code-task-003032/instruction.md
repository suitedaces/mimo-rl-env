Cannot declare that boolean values do not accept an argument.
I'd like the ability to tell yargs-parser that boolean arguments do not accept values in the next argument.  Lets say I have `mytest.js`:
```js
#!/usr/bin/env node
'use strict';

const argv = require('yargs-parser')(process.argv.slice(2), {
	boolean: ['all'],
	narg: {
		all: 0
	},
	configuration: {
		'halt-at-non-option': true
	}
});
console.log(argv);
```

Currently:
```
$ ./mytest.js --all echo hi
{ _: [ 'echo', 'hi' ], all: true }
$ ./mytest.js --all true
{ _: [], all: true }
$ ./mytest.js --all false
{ _: [], all: false }
$ ./mytest.js --no-all true
{ _: [ 'true' ], all: false }
$ ./mytest.js --no-all false
{ _: [ 'false' ], all: false }
```

I feel that `narg: {all: 0}` should tell yargs-parser that `--all` should be processed without looking at the next argument.  I think it's only valid to set `narg` of a boolean to 0 or 1.  The following shows the desired output for the currently failing test cases:
```
$ ./mytest.js --all true
{ _: [ 'true' ], all: true }
$ ./mytest.js --all false
{ _: [ 'false' ], all: true }
```
