## `child_process.spawn` doesn't emit `'error'` when the command can't be started

I'm writing a small Node.js script that shells out to an external program with `child_process.spawn`. I want to handle the case where the program isn't installed (or the path is wrong) so I can show the user a friendly message instead of crashing.

According to the docs, `'error'` is the event I'm supposed to listen on for things like "the child process failed to start". So I wrote:

```js
var spawn = require('child_process').spawn;

var child = spawn('definitely_not_a_real_binary', ['--foo']);

child.on('error', function(err) {
  console.log('error event:', err);
});

child.on('exit', function(code, signal) {
  console.log('exit event:', code, signal);
});
```

I expected my `'error'` handler to fire with some kind of `Error` object I could inspect (errno / code / syscall) so I'd know it was a "command not found" situation versus something else.

What I actually see:

- `'error'` never fires.
- `'exit'` fires instead, and I just get back some numeric code with no extra information. There's no `Error` object anywhere — I can't tell from the exit handler whether the child actually ran and failed, or whether it never started at all.

This makes it pretty awkward to write robust code around `spawn`. The synchronous path (where `spawn` throws straight away) is fine, but the failures that surface later through the child handle look indistinguishable from a normal child process that just happened to exit with a nonzero status.

It would be much nicer if a failure to actually start the child were reported via the `'error'` event with a proper `Error` (carrying the underlying errno / syscall info), and not as a regular `'exit'`.
