toHaveTextContent should support any Node
- `@testing-library/jest-dom` version: 5.11.5
- `node` version: 12.18.0
- `yarn` version: 1.22.5
- `react-testing-library` version: 11.1.0

### Relevant code or config:

```js
    const resourceLabel = getByText('Resource:');
    const valueElement = ensureExists(resourceLabel.nextSibling);
    expect(valueElement).toHaveTextContent('libxul.so');
```

### What you did:

I'm in the process of installing and using jest-dom in our project. I installed the eslint plugin which converted this code:
```js
    const resourceLabel = getByText('Resource:');
    const valueElement = ensureExists(resourceLabel.nextSibling);
    expect(valueElement.textContent).toBe('libxul.so');
```

### What happened:
Here is the error I get:
```
    received value must be an HTMLElement or an SVGElement.
    Received has type:  object
    Received has value: libxul.so

       95 |     const resourceLabel = getByText('Resource:');
       96 |     const valueElement = ensureExists(resourceLabel.nextSibling);
    >  97 |     expect(valueElement).toHaveTextContent('libxul.so');

```

### Reproduction:
https://codesandbox.io/s/react-testing-library-demo-forked-0puq7

### Problem description:

The property `textContent` is present in all `Node`s, not only `HTMLElement`. Therefore it would be nice if this expectation worked on all `Node`s too, especially text nodes.

See the MDN page about `textContent`:
https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent

### Suggested solution:
Is removing this line enough:
https://github.com/testing-library/jest-dom/blob/c11f9c53bbf94c1aa48b401f4f523500e904e128/src/to-have-text-content.js#L8

Or should we replace it with a check for `instanceof Node` ?
