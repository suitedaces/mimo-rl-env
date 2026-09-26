## slate-hyperscript: can't build intentionally-invalid values, and bare `<document>` produces extra text nodes

I'm using `slate-hyperscript` to write test fixtures and ran into two things that look wrong.

### 1. `<value>` always normalizes — can't test validation logic

I'm writing tests for some schema / validation rules. The natural way is to hand-build a value that violates a rule and then assert that my validation code catches/fixes it. But when I build that value with hyperscript, hyperscript itself silently fixes it before my code even runs, so the test can't actually exercise the validation path.

For test fixtures I'd really like a way to say "give me back exactly the tree I described, even if it's not strictly valid" — otherwise hyperscript hides the very bugs I'm trying to test.

### 2. Bare `<document>` / `<block>` adds a phantom empty text node

Separately, I noticed that if I don't wrap things in `<value>` and just build a document directly, the resulting `document.nodes` doesn't match what I wrote. There's an extra empty text node tacked on at the end that I didn't put there.

Roughly:

```js
const doc = (
  <document>
    <block type="paragraph">hello</block>
    <block type="paragraph">world</block>
  </document>
)

// doc.nodes ends with an unexpected empty text node after the two paragraphs
```

I didn't catch this earlier because I usually wrap in `<value>`, and apparently the normalization that runs there cleans the stray node up. As soon as I stopped going through `<value>` it showed up.

These two issues actually interact — fixing #1 (so I can opt out of normalization on `<value>`) makes #2 visible there too, so both should be addressed.

For the opt-out in #1, I'd expect something like `<value normalize={false}>...</value>` — i.e. a `normalize` attribute on the `<value>` tag.
