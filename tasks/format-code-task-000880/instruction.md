RegExp() (without new) fails under ses-0.7.3 unless noTameRegExp is enabled
I tried loading the `tap` unit-testing library in a SES-locked-down environment, and got an error I don't understand.

Clone [this gist repo](https://gist.github.com/warner/dfde9f05c3d80497ac9aa2c72493506a) and run `yarn` and `node -r esm main.js`. This imports one module (which imports `lockdown` and calls it), then imports a second module (which imports `tap`). The error I get (under node-13.7.0) is:

```
$ node -r esm main.js
did lockdown()

/tmp/dfde9f05c3d80497ac9aa2c72493506a/node_modules/ses/dist/ses.cjs:2779
    return Reflect.construct(unsafeRegExp, arguments, new.target);
                   ^
/tmp/dfde9f05c3d80497ac9aa2c72493506a/node_modules/ses/dist/ses.cjs:1
TypeError: undefined is not a constructor
    at RegExp (/tmp/dfde9f05c3d80497ac9aa2c72493506a/node_modules/ses/dist/ses.cjs:2779:20)
    at Object.<anonymous> (/tmp/dfde9f05c3d80497ac9aa2c72493506a/node_modules/tap/node_modules/yaml/dist/tags/yaml-1.1/timestamp.js:72:9)
    at Object.Module._compile (/tmp/dfde9f05c3d80497ac9aa2c72493506a/node_modules/source-map-support/source-map-support.js:541:25)
    at Object.Module._extensions..js (internal/modules/cjs/loader.js:1171:10)
```


This may be a matter of `tap` not being compatible with SES, but 1) maybe we can figure out the problem and fix it, and 2) it's interfering with the #216 ses-adapter work. This pattern, where we lock everything down via an import at the beginning of the application, then import everything else, is our main plan for using `ses-adapter`.

I looked a little bit closer, and noticed that the `yaml` module in the stack trace is calling `RegExp` without a `new`.. not sure if that's significant or not:

```js
const timestamp = {
  identify: value => value instanceof Date,
  default: true,
  tag: 'tag:yaml.org,2002:timestamp',
  // If the time zone is omitted, the timestamp is assumed to be specified in UTC. The time part
  // may be omitted altogether, resulting in a date format. In such a case, the time part is
  // assumed to be 00:00:00Z (start of day, UTC).
  test: RegExp('^(?:' + '([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})' + // YYYY-Mm-Dd
  '(?:(?:t|T|[ \\t]+)' + // t | T | whitespace
  '([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2}(\\.[0-9]+)?)' + // Hh:Mm:Ss(.ss)?
  '(?:[ \\t]*(Z|[-+][012]?[0-9](?::[0-9]{2})?))?' + // Z | +5 | -03:30
  ')?' + ')$'),
...
```
