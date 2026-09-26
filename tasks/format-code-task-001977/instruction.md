Object-based API
I'm considering a breaking API change that will make RBush more performant, but also more verbose, by replacing internal representation of bounding boxes from a 4-length array to a 4-property object. V8 handles object literals faster, and this also allows simplifying some internal logic. API-wise, this would look like this:

``` js
// before
tree.insert([20, 40, 30, 50]);
tree.search([5, 6, 10, 12]);

// after
tree.insert({minX: 20, minY; 40, maxX: 30, maxY: 50});
tree.search({minX: 5, minY: 6, maxX: 10, maxY: 12});
```

You would still be able to configure a custom format for inserted items, but would have to change `search` to use object literals for bbox instead of arrays in any case.

The tree node JSON format would also change:

``` js
// before
{
  children: [...],
  height: 1,
  bbox: [0, 0, 20, 20],
  leaf: true
}

// after
{
  children: [...],
  height: 1,
  minX: 0,
  minY: 0,
  maxX: 20,
  maxY: 20,
  leaf: true
}
```

This is implemented in `memory-perf` branch that I'm increasingly using in my new algorithmic experiments. The benchmark results (in Node 6.2.2) are as follows:

``` bash
# master, items: 1000000, nodeSize: 16
insert one by one: 4969.933ms
1000 searches 10%: 2534.136ms
1000 searches 1%: 472.504ms
1000 searches 0.01%: 61.429ms
remove 1000 one by one: 26.362ms
bulk-insert 1M more: 1506.807ms
1000 searches 1%: 839.277ms
1000 searches 0.01%: 107.652ms

# memory-perf, items: 1000000, nodeSize: 16
insert one by one: 3523.986ms
1000 searches 10%: 2202.467ms
1000 searches 1%: 345.745ms
1000 searches 0.01%: 31.921ms
remove 1000 one by one: 30.391ms
bulk-insert 1M more: 1226.326ms
1000 searches 1%: 610.299ms
1000 searches 0.01%: 71.066ms
```

@twpayne @tschaub @mbloch @oscarlorentzon @vkurchatkin @bhousel — does this sound acceptable? I would bump the major version for this of course.
