## `getFormProps` / `getFieldsetProps` shouldn't emit `aria-invalid`

I'm spreading the helpers onto my form and fieldset like this:

```tsx
<form {...getFormProps(form)}>
  ...
  <fieldset {...getFieldsetProps(fields.address)}>
    ...
  </fieldset>
</form>
```

When the form has errors I noticed in DevTools that the rendered markup contains:

```html
<form aria-invalid="true" aria-describedby="..."> ... </form>
<fieldset aria-invalid="true" aria-describedby="..."> ... </fieldset>
```

This doesn't look right. Per the ARIA spec, `aria-invalid` is meant for elements that actually accept user input (textbox / checkbox / radio / combobox / etc.). `<form>` and `<fieldset>` are grouping/container elements, not input widgets, so putting `aria-invalid` on them isn't appropriate — and a11y linters flag it.

I'd expect Conform to only set `aria-invalid` automatically on the real form controls (the things you get back from `getInputProps` / `getTextareaProps` / `getSelectProps` / `getCollectionProps`). It shouldn't be part of the props returned by `getFormProps` or `getFieldsetProps`.

`aria-describedby` on the form/fieldset is fine — that one is valid on container elements and it's still useful for pointing at the form-level error summary.

So my ask is just: drop `aria-invalid` from the output of `getFormProps` and `getFieldsetProps`, while leaving the input-level helpers untouched.
