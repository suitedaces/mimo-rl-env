Regression: LogicalExpression in ConditionalExpression.test is not aligned
**Prettier pr-5039**
[Playground link](https://deploy-preview-5039--prettier.netlify.com/playground/#N4Igxg9gdgLgprEAuc0wEMYAoDaAdKAAkKggBM4A6AMwEsAnAZxgGEALWgGzMpgE8ADnEIBeMYTwh4ADxiTCAMgUFipCjQbN2XHrUYB1DvADKA9GDjGEjWjFoA3YUpUlyVOk1YdulPQEkoClhMWmgrKBs7RxdiAH5CTls4enRORKg4GMIkV3UPLW8eNnRGABk4dDJaKABzU3M4RkVlImI2tXdNLx1fMoqq2vqLcMiHTNa4hOrxtuzCRghqGHS4ABoXAXpq7u56BCwzGDZVwggBO2hGE83tgEoCAF1bgG4CEFWQM4uI5FB0enoEAA7gAFf7WZAgdD2CC0MjvEAAIxSYAA1nAYENqjVkDB6ABXNYgNgwAC2nEMSUYZmG1lsDlsfEhYEYjAR1UYyRgIJSNVJ6GQ1FSnI+ACtGNIAEIo9GY9CkuClaaC4VEsxMZKQxHoRF8TjQBE3WD6OFHZAADgADB9NhBOfoUgJIZtGslHAi9gBHfEMOA89B8gVIIWcEUgTmk2i4glEmy1ThwACK+Ig8BVoaJMB1JrIZqQACYPnj0FxsSwIKT+ZDSBkEfjOQAVHVs4OqgC+baAA)
```sh
--parser babylon
```

**Input:**
```jsx
concat([
  node.firstChild.type === "text" &&
  node.firstChild.isWhiteSpaceSensitive &&
  node.firstChild.isIndentationSensitive
    ? literalline
    : node.firstChild.hasLeadingSpaces &&
      node.firstChild.isLeadingSpaceSensitive
    ? line
    : softline,
  printChildren(path, options, print)
]);

```

**Output:**
```jsx
concat([
  node.firstChild.type === "text" &&
  node.firstChild.isWhiteSpaceSensitive &&
  node.firstChild.isIndentationSensitive
    ? literalline
    : node.firstChild.hasLeadingSpaces &&
    node.firstChild.isLeadingSpaceSensitive
    ? line
    : softline,
  printChildren(path, options, print)
]);

```

**Expected behavior:**
Same as input.

Regression from #5039, cc @suchipi @duailibe
