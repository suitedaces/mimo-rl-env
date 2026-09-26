## Make the init callback optional

When constructing a Lawnchair instance with a synchronous adapter (e.g. localStorage), there's no real reason to pass a callback — the store is ready immediately. But right now Lawnchair refuses to construct without one:

```js
// throws: "No callback was provided"
var store = new Lawnchair({ name: 'things' });

// also throws: "Incorrect # of ctor args!"
var store = new Lawnchair();
```

So in practice a lot of code ends up looking like:

```js
new Lawnchair({ name: 'things' }, $.noop);
new Lawnchair({ name: 'things' }, Prototype.emptyFunction);
new Lawnchair({ name: 'things' }, function(){});
```

…just to get past the constructor check. That's noise — the user clearly doesn't care about being notified, especially against a synchronous backend.

Could the callback be made optional? I'd expect all of these to just work:

```js
new Lawnchair();
new Lawnchair({ name: 'things' });
new Lawnchair(function (ref) { /* ... */ });
new Lawnchair({ name: 'things' }, function (ref) { /* ... */ });
```

i.e. you can pass options, a callback, both, or nothing, and Lawnchair still constructs cleanly.
