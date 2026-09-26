## `selectAll` returns descendants of `<template>` elements

When querying HTML that contains a `<template>` tag, css-select returns elements that live *inside* the template, even though browsers don't expose those to normal CSS queries.

### Repro

```js
import { parseDocument } from "htmlparser2";
import { selectAll } from "css-select";

const doc = parseDocument(`
  <div class="outer">hello</div>
  <template>
    <div class="inside-template">should be hidden</div>
  </template>
`);

console.log(selectAll("div", doc).map(el => el.attribs.class));
// => [ 'outer', 'inside-template' ]
```

In a real browser, `document.querySelectorAll('div')` on the same markup only returns the outer `div` — the contents of `<template>` are inert and not reachable via ordinary selector queries.

This is also showing up downstream in cheerio (https://github.com/cheeriojs/cheerio/issues/2643), where users pulling data out of pages with templates are getting unexpected hits from inside the template.

It would be nice if `selectAll` (and friends) matched the browser behavior by default for HTML documents and didn't descend into `<template>` elements.
