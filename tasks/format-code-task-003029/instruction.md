Unexpected behavior of `strict()` with extra args
I'm writing commands using `commandDir()` and want to enable strict mode. However, strict mode doesn't seem to catch when extra arguments are inserted in the middle of the command. Here's my scenario:

Yargs version: 7.0.2
Node version: 6.10.0

**Folder Structure**
```
index.js
commands/
    command.js
```

**`index.js`**
```js
const yargs = require('yargs');

yargs
    .commandDir('commands')
    .demandCommand(1)
    .strict()
    .help()
    .argv;
```

**`commands/command.js`**
```js
exports.command = 'command <param>';
exports.desc = 'Some sub-command';

exports.builder = (yargs) => {
    return yargs
        .strict(); // Don't think this is necessary, but just in case
};

exports.handler = (args) => {
    console.log(args.param);
};
```

When i run the following, everything is normal:

```
$ node index.js command foo
foo
```

However, when i add an extra non-hyphenated argument in the middle, things get strange:

```
$ node index.js imposter command foo
command
```

Not only does strict mode not fail the command, it seems to both match the command in `command.js` and treat it as if 'imposter' is the command and 'command' is the parameter.

Am I missing something here? I was hoping that strict mode would fail the command, but it seems like it should at least print `foo` in both cases
