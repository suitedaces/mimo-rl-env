The iteration methods on this library don't behave like the native `Array.prototype` ones when it comes to `this` binding.

Native `Array#forEach`, `map`, `filter`, `find`, `every`, `some`, etc. all accept an optional second argument that becomes `this` inside the callback, and they invoke the callback with `(value, index, array)`. The methods here don't — they call the callback as a plain function and only pass `(value, index)`.

This makes it painful to use these helpers from inside a class / object that holds state. For example:

```js
function Filter(threshold) {
  this.threshold = threshold;
}

Filter.prototype.run = function(items) {
  // items is an enumerable from this lib
  return items.filter(function(item) {
    return item.score > this.threshold;   // `this` is not my Filter instance
  }, this);
};
```

With native arrays this works fine — the second arg to `filter` is used as `this` inside the callback. With this library it doesn't, so I end up having to `.bind(this)` or stash a `var self = this` everywhere I touch one of these enumerables, which gets noisy fast.

Same story for the other iteration helpers (`each`/`forEach`, `map`, `find`, `every`/`all`, `some`/`any`, `none`, `count`, etc.) — none of them let me pass a `this` value, and the callback signature doesn't include the source collection either, so callbacks that want to look at the whole thing can't.

Could the enumerable helpers be lined up with the native `Array.prototype` callback conventions?
