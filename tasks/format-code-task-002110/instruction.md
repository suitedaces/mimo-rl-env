## Feature request: built-in `reverse` for arrays

Cadence arrays come with a few non-mutating helpers like `slice` and `concat`, but I can't find any built-in way to get the contents of an array back in reversed order. Whenever I need it I end up writing the same kind of manual loop:

```cadence
let xs: [Int] = [1, 2, 3, 4]
let reversed: [Int] = []
var i = xs.length - 1
while i >= 0 {
    reversed.append(xs[i])
    i = i - 1
}
```

It's pretty verbose for something that feels like it should be a one-liner. I'd love to be able to do something like `xs.reverse()` and get back `[4, 3, 2, 1]` as a fresh array, with the original left untouched. This should work uniformly on both `[T]` and `[T; N]` so I don't have to think about which array flavour I'm holding.

Since reversing here means producing a new array containing the same elements, it only really makes sense when the elements can be copied. For arrays of resources there's no sensible way to do it — a resource value can't just be duplicated into a second array — so I'd expect this helper to simply not be available on resource-typed arrays, the same way other copy-style array operations aren't allowed there.

Tracked by #2605.
