## `no-redundant-story-name` doesn't catch redundant names in CSF2 stories

I have a project with a lot of CSF2-style stories, e.g.:

```js
export const PrimaryButton = () => <Button primary />
PrimaryButton.storyName = 'Primary Button'
```

Here `'Primary Button'` is exactly what Storybook would generate from the export name `PrimaryButton`, so the `storyName` assignment is redundant and I'd expect `no-redundant-story-name` (which I have enabled via the recommended config) to flag it. But running ESLint on this file produces no warnings.

The rule does seem to fire on CSF3 stories that use a `name` property:

```js
export const PrimaryButton = {
  name: 'Primary Button',
  render: () => <Button primary />,
}
```

but I also tried the CSF3-with-`storyName` variant:

```js
export const PrimaryButton = {
  storyName: 'Primary Button',
  render: () => <Button primary />,
}
```

and that one isn't flagged either, even though `storyName` is a valid alias of `name` in Storybook's story API.

It would be great if this rule worked for both CSF2 (`Story.storyName = '...'`) and CSF3 stories, and recognized both `name` and `storyName` as the property to check.
