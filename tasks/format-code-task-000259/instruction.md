[BUG] :filter filter run does not always remove non-matching entries (linked-list.js issue)
### Describe the bug

I expect the output of the filter expression `A =A B =A :filter[match[B]]` to be `B`, but the output is `B A`

Looks to me like an issue with `linked-list-.js` not removing items correctly. If I add this line to `editions/test/tiddlers/tests/test-linked-list.js`:

```js
compare(remove(newPair(["A", "A", "B", "A"]), ["A", "A", "A"])); // B
```

Then I get this test failure when running the test suite:

```
Failures:
1) LinkedList class tests can remove all instances of a multi-instance value
  Message:
    Expected $.length = 2 to equal 1.
    Unexpected $[1] = 'A' in array.
  Stack:
    Error: Expected $.length = 2 to equal 1.
    Unexpected $[1] = 'A' in array.
        at <Jasmine>
        at compare (test-linked-list.js:64:35)
        at UserContext.<anonymous> (test-linked-list.js:111:7)
        at <Jasmine>
  Message:
    Expected 2 to be 1.
  Stack:
    Error: Expected 2 to be 1.
        at <Jasmine>
        at compare (test-linked-list.js:65:32)
        at UserContext.<anonymous> (test-linked-list.js:111:7)
        at <Jasmine>
```

### Expected behavior

The `:filter` filter run should remove all non-matching entries from the input

### To Reproduce

1. Paste `A =A B =A :filter[match[B]]` into https://tiddlywiki.com/#%24%3A%2FAdvancedSearch filter tab
2. See the unexpected results `B A`

### Screenshots

_No response_

### TiddlyWiki Configuration

- Version v5.2.3


### Additional context

_No response_
