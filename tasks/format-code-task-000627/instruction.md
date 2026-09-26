## Feature request: a `with*`-style helper to scope DOM activities to a CSS/XPath selector

I'm writing CasperJS scripts against pages that contain several visually similar "panels" (think modals, cards, repeated widgets). Each panel has the same internal structure — same class names, same input names, same buttons — just inside a different container. So when I do something like:

```js
casper.then(function () {
    this.click('.submit-button');
    this.fill('form.editor', { name: 'foo' }, true);
});
```

…the selectors are ambiguous and I have to remember to manually prefix every single one with the container, e.g. `'#panel-2 .submit-button'`, `'#panel-2 form.editor'`, and so on. It's verbose, easy to forget on one of the calls, and it makes the test code harder to read because the panel I'm "in" is repeated on every line instead of being said once.

CasperJS already ships a really nice family of helpers for the equivalent problem on a different axis:

- `withFrame(frameInfo, then)` — switches the DOM context to a given frame, runs the step, and automatically reverts when the step finishes.
- `withPopup(popupInfo, then)` — same idea but for popups.

Both of them solve exactly the "say it once, scope everything inside, auto-revert when done" problem — but only for frames and popups. There doesn't seem to be an equivalent for "scope everything inside this element on the current page", which is by far the most common case I run into.

What I'd like is a sibling helper in that same family that takes a CSS3 / XPath selector instead of a frame name or popup info, so I could write something like:

```js
casper.start('http://example.com/dashboard');

// everything inside this `then` is implicitly scoped to #panel-2
casper.<scope-helper>('#panel-2', function () {
    this.click('.submit-button');     // resolves inside #panel-2 only
    this.fill('form.editor', { name: 'foo' }, true);
    this.test.assertExists('.success-message');
});

// back to the full document automatically
casper.then(function () {
    this.test.assertExists('#global-toolbar');
});

casper.run();
```

The behavioural contract I'm hoping for is the same as `withFrame` / `withPopup`:

- the scope switch lasts only for the duration of the step passed in;
- once that step is done, the scope is restored to whatever it was before (the document by default), so the next `casper.then(...)` is back to operating on the whole page;
- it should accept the same kind of selector argument the rest of CasperJS already takes (CSS3 string or XPath object).

This would make tests against pages with repeated structures dramatically cleaner and remove a whole class of "I forgot to prefix one selector" bugs. Would you be open to adding something like this to the `with*` family?

A natural name for this new helper, to stay consistent with `withFrame` / `withPopup`, would be something like `withSelectorScope(selector, then)`.
