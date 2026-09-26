Process streams uncaught exceptions when `buffer: false` is used
When the `buffer: false` option is used, any error on the child process streams creates an uncaught exception. For example, this crashes the current process:

```js
const subprocess = execa('echo', {buffer: false, reject: false});
subprocess.stdout.destroy(new Error('test'));
await subprocess
```
