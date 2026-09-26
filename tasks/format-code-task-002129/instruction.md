## `no-redundant-role` flags `<nav role="navigation">` and bare elements without any role

I'm using `eslint-plugin-lit-a11y` to lint the lit-html templates in my web components. Two false positives are getting in the way:

### 1. `<nav role="navigation">` is reported as redundant

```js
html`
  <nav role="navigation">
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
`;
```

The `no-redundant-role` rule fires on this and tells me `"navigation"` role is implicit in `<nav>`, so I should drop the attribute. The thing is, explicitly setting `role="navigation"` on `<nav>` is a long-standing accessibility recommendation — there are screen reader / older browser combinations that don't expose the implicit landmark role correctly, and putting the role on explicitly is the documented workaround. Plenty of a11y guides (and the WAI-ARIA authoring practices around landmarks) still suggest doing it. So I'd really like the rule to not punish me for this specific pairing.

### 2. The rule also fires on elements that have no role at all

I noticed regular elements like a plain `<div>` (no `role` attribute, and no implicit role either) are also being flagged. Something like:

```js
html`<div>hello</div>`;
```

reports a "redundant role" warning, which doesn't make sense — there's no role on the element and the element doesn't have a default one either, so there's nothing redundant going on. Looks like the comparison isn't accounting for the case where neither role exists.

Could the rule be adjusted so that (1) the `nav` + `navigation` pairing is allowed, and (2) elements with no implicit *and* no explicit role aren't reported? Thanks!
