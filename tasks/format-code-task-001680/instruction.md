## Feature request: custom value transformation for non-builtin types (e.g. Buffer)

I'm using jsonexport to dump a list of records to CSV. Some of the fields in my records are `Buffer` instances (binary / encoded data coming from a database). What I actually want in the CSV is just `buffer.toString()`, but currently jsonexport doesn't seem to know what to do with a Buffer — it falls through to the generic object handling and explodes it into a bunch of meaningless sub‑columns (the internal shape of the Buffer object), instead of treating the whole Buffer as a single value.

A reduced example of what I'm passing in:

```js
const jsonexport = require('jsonexport');

const contacts = {
  a: Buffer.from('a2b', 'utf8'),
  b: Buffer.from('other field', 'utf8'),
  x: 22,
  z: function () { return 'bad ace'; },
};

jsonexport(contacts, function (err, csv) {
  console.log(csv);
});
```

The Buffer fields don't come out as `a2b` / `other field`, and the function-valued field `z` similarly has no clean way to be turned into the string I actually want.

Looking at the docs, I can customize **strings**, **numbers**, **booleans** and **dates** through `handleString` / `handleNumber` / `handleBoolean` / `handleDate`. But there's no equivalent hook for "I have a value of type X (where X is some class like Buffer, or even just a plain `Function`), please run *my* function over it before serialising". So right now I'd have to walk my whole input and pre-stringify every Buffer myself before handing it to jsonexport, which kind of defeats the purpose of using the library on nested structures.

It would be great if the options accepted some user-supplied mapping from a type to a transform function, so I could express things like:

- "if the value is a `Buffer`, replace it with `value.toString()` before serialising"
- "if the value is a `Function`, call it and use the return value"
- and in general add my own classes there too

Ideally the transform callback should also receive a bit of context — not just the value itself, but also where it sits in the parent (the property key when the parent is an object, the index when the parent is an array) and a reference to the parent — because for some of my fields the right transformation depends on which field it is, not just its type.

Existing `handleString` / `handleNumber` / `handleBoolean` / `handleDate` options should keep working for backward compatibility, though once a more general type-based mechanism exists, they're basically a strict subset of it and could probably be marked deprecated.

I'd imagine exposing this as a new option something like `typeHandlers` on the options object.
