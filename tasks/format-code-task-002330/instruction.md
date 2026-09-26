## `<!-- prettier-ignore -->` doesn't fully protect an inline element that immediately follows it

I use `<!-- prettier-ignore -->` to keep certain HTML lines exactly the way I wrote them — typically short, tightly packed inline elements where the line break placement matters to me.

I noticed prettier still reformats the element on the very next line, even though I told it to ignore that element.

### Input

```html
<!--prettier-ignore--><span></span>
<!--prettier-ignore--><span>_</span>
```

### What I get from prettier

```html
<!--prettier-ignore--><span
></span>
<!--prettier-ignore--><span>_</span>
```

The empty `<span></span>` got broken across two lines. The non-empty one right below it was left alone, which is what I'd expect for both.

To make it worse, if I run prettier on the already-formatted output a second time, it gets even worse and inserts an extra blank line inside the tag:

```html
<!--prettier-ignore--><span

></span>
<!--prettier-ignore--><span>_</span>
```

So every save keeps drifting the formatting further from what I originally wrote.

### What I expect

`<!-- prettier-ignore -->` should leave the element on the next line completely untouched, including the empty `<span></span>` case. And formatting an already-formatted file shouldn't keep changing it.
